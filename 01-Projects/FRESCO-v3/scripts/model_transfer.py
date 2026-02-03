#!/usr/bin/env python3
"""Phase 3: modeling for zero-shot transfer (local proxy).

Trains on source-cluster labeled jobs and evaluates on target-cluster jobs.
This is a local-proxy implementation using EXP-001 job_partials parquet outputs.

Label is configurable; for the local proxy we use value_memused_max as a stand-in
for peak memory, and report results as *proxy-only*.

Writes:
- results/metrics.json
- results/predictions_source_test.parquet
- results/predictions_target.parquet
- manifests/run_metadata.json + input_files_used.json
- validation/python_version.txt + pip_freeze.txt
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import random
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from sklearn.impute import SimpleImputer
from sklearn.linear_model import HuberRegressor, Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def _utc_now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def _git_info(git_root: Path) -> dict:
    info: dict = {}
    rc, out, _ = _run(["git", "rev-parse", "HEAD"], git_root)
    info["git_commit"] = out.strip() if rc == 0 else None
    rc, out, _ = _run(["git", "status", "--porcelain=v1"], git_root)
    info["git_status_porcelain"] = out if rc == 0 else None
    return info


def _load_manifest_rows(manifest_path: Path, cluster: str) -> list[dict]:
    rows = json.loads(manifest_path.read_text(encoding="utf-8"))
    return [r for r in rows if r.get("cluster") == cluster]


def _read_parquets(
    manifest_rows: list[dict],
    columns: list[str],
    max_rows: int,
    seed: int,
) -> tuple[pd.DataFrame, list[Path]]:
    rng = random.Random(seed)
    paths = [Path(r["path"]) for r in manifest_rows]
    rng.shuffle(paths)

    dfs: list[pd.DataFrame] = []
    used: list[Path] = []
    n = 0

    for p in paths:
        if n >= max_rows:
            break

        pf = pq.ParquetFile(str(p))
        available = set(pf.schema_arrow.names)
        col_subset = [c for c in columns if c in available]
        tbl = pf.read(columns=col_subset)
        df = tbl.to_pandas()
        for c in columns:
            if c not in df.columns:
                df[c] = np.nan

        remaining = max_rows - n
        if len(df) > remaining:
            df = df.sample(remaining, random_state=seed)

        if len(df) > 0:
            dfs.append(df[columns])
            used.append(p)
            n += len(df)

    if not dfs:
        return pd.DataFrame(columns=columns), []

    out = pd.concat(dfs, ignore_index=True)

    # job_partials can contain multiple rows per jid (partials/time slices). Collapse to job-level.
    if "jid" in out.columns:
        numeric_cols = [c for c in columns if c != "jid"]
        for c in numeric_cols:
            out[c] = pd.to_numeric(out[c], errors="coerce")
        out = out.groupby("jid", as_index=False)[numeric_cols].max()
        out = out[["jid"] + numeric_cols]

    return out[columns], used


def _derive_cpu_standard(df: pd.DataFrame) -> pd.Series:
    gpu_cnt = df.get("value_gpu_cnt")
    gpu_sum = df.get("value_gpu_sum")
    if gpu_cnt is None and gpu_sum is None:
        return pd.Series([True] * len(df))
    gpu_cnt = pd.to_numeric(gpu_cnt, errors="coerce").fillna(0)
    gpu_sum = pd.to_numeric(gpu_sum, errors="coerce").fillna(0)
    return (gpu_cnt <= 0) & (gpu_sum <= 0)


def _smape_median(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    denom = np.abs(y_true) + np.abs(y_pred) + 1e-8
    return float(np.median(2 * np.abs(y_true - y_pred) / denom) * 100.0)


def _evaluate(y_true_log: np.ndarray, y_pred_log: np.ndarray) -> dict:
    y_true = np.expm1(y_true_log)
    y_pred = np.expm1(y_pred_log)
    resid = y_true_log - y_pred_log

    # Calibration: y_true_log ≈ slope * y_pred_log + intercept
    A = np.vstack([y_pred_log, np.ones_like(y_pred_log)]).T
    slope, intercept = np.linalg.lstsq(A, y_true_log, rcond=None)[0]

    return {
        "r2": float(r2_score(y_true_log, y_pred_log)),
        "mae_log": float(mean_absolute_error(y_true_log, y_pred_log)),
        "mdae_log": float(np.median(np.abs(resid))),
        "smape": _smape_median(y_true, y_pred),
        "bias_log": float(np.mean(resid)),
        "slope": float(slope),
        "intercept": float(intercept),
    }


def _bootstrap_r2(y_true_log: np.ndarray, y_pred_log: np.ndarray, n_boot: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    n = len(y_true_log)
    if n == 0:
        return {"r2_mean": None, "r2_ci_lower": None, "r2_ci_upper": None}

    stats = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        stats.append(r2_score(y_true_log[idx], y_pred_log[idx]))

    stats = np.array(stats, dtype=float)
    return {
        "r2_mean": float(np.mean(stats)),
        "r2_ci_lower": float(np.quantile(stats, 0.025)),
        "r2_ci_upper": float(np.quantile(stats, 0.975)),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    cfg_path = (repo_root / args.config).resolve()
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    run_id = cfg["run_id"]
    exp_dir = (repo_root / "experiments" / run_id).resolve()
    for d in ["config", "logs", "results", "manifests", "validation"]:
        (exp_dir / d).mkdir(parents=True, exist_ok=True)

    # Copy config into run folder for provenance
    (exp_dir / "config" / Path(cfg_path).name).write_text(cfg_path.read_text(encoding="utf-8"), encoding="utf-8")

    log_path = exp_dir / "logs" / "model_transfer.log"

    def log(msg: str) -> None:
        line = f"[{_utc_now_iso()}] {msg}"
        print(line)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    seed = int(cfg.get("random_seed", cfg.get("split", {}).get("seed", 1337)))
    random.seed(seed)
    np.random.seed(seed)

    source = cfg["source_cluster"]
    target = cfg["target_cluster"]
    regime = cfg.get("regime", "cpu_standard")
    label_col = cfg["label_column"]
    label_transform = cfg.get("label_transform", "log1p")
    feature_cols = list(cfg["feature_columns"])
    max_src = int(cfg.get("max_rows_source", 200000))
    max_tgt = int(cfg.get("max_rows_target", 200000))
    n_boot = int(cfg.get("n_boot", 200))

    overlap = cfg.get("overlap_run", {})
    matched_source_idx = (repo_root / overlap["matched_source_indices"]).resolve()
    matched_target_idx = (repo_root / overlap["matched_target_indices"]).resolve()

    log(f"run_id={run_id}")
    log(f"config={cfg_path}")
    log(f"source={source} target={target} regime={regime}")
    log(f"label={label_col} transform={label_transform}")
    log(f"features={feature_cols}")
    log(f"matched_source_indices={matched_source_idx}")
    log(f"matched_target_indices={matched_target_idx}")

    src_jids = set(pd.read_parquet(matched_source_idx)["jid"].astype("string").tolist())
    tgt_jids = set(pd.read_parquet(matched_target_idx)["jid"].astype("string").tolist())

    manifest_path = (repo_root / cfg["inputs_manifest"]).resolve()
    src_rows = _load_manifest_rows(manifest_path, source)
    tgt_rows = _load_manifest_rows(manifest_path, target)
    if not src_rows or not tgt_rows:
        raise FileNotFoundError("Missing manifest rows for source/target")

    needed = ["jid", label_col] + feature_cols + ["value_gpu_cnt", "value_gpu_sum"]
    needed = list(dict.fromkeys(needed))

    log("loading source data...")
    src, src_used = _read_parquets(src_rows, needed, max_rows=max_src, seed=seed)
    log(f"source_rows_loaded={len(src)} source_files_used={len(src_used)}")

    log("loading target data...")
    tgt, tgt_used = _read_parquets(tgt_rows, needed, max_rows=max_tgt, seed=seed + 1)
    log(f"target_rows_loaded={len(tgt)} target_files_used={len(tgt_used)}")

    if regime == "cpu_standard":
        src = src.loc[_derive_cpu_standard(src)].copy()
        tgt = tgt.loc[_derive_cpu_standard(tgt)].copy()

    # Filter to matched overlap cohorts
    src = src.loc[src["jid"].astype("string").isin(src_jids)].copy()
    tgt = tgt.loc[tgt["jid"].astype("string").isin(tgt_jids)].copy()

    log(f"source_rows_after_filters={len(src)} target_rows_after_filters={len(tgt)}")

    # Clean + transform
    for c in feature_cols:
        src[c] = pd.to_numeric(src[c], errors="coerce")
        tgt[c] = pd.to_numeric(tgt[c], errors="coerce")

    src[label_col] = pd.to_numeric(src[label_col], errors="coerce")
    tgt[label_col] = pd.to_numeric(tgt[label_col], errors="coerce")

    # Require positive label
    src = src.loc[src[label_col].notna() & (src[label_col] > 0)].copy()
    tgt = tgt.loc[tgt[label_col].notna() & (tgt[label_col] > 0)].copy()

    if label_transform == "log1p":
        y_src = np.log1p(src[label_col].to_numpy(dtype=float))
        y_tgt = np.log1p(tgt[label_col].to_numpy(dtype=float))
    else:
        raise ValueError(f"Unsupported label_transform: {label_transform}")

    # Features: use log1p for heavy-tailed allocations
    X_src = src[feature_cols].copy()
    X_tgt = tgt[feature_cols].copy()
    for c in feature_cols:
        X_src[c] = np.log1p(X_src[c])
        X_tgt[c] = np.log1p(X_tgt[c])

    split = cfg.get("split", {"type": "random", "test_frac": 0.2, "seed": seed})
    test_frac = float(split.get("test_frac", 0.2))
    rng = np.random.default_rng(int(split.get("seed", seed)))

    n_src = len(X_src)
    idx = np.arange(n_src)
    rng.shuffle(idx)
    n_test = int(round(test_frac * n_src))
    test_idx = idx[:n_test]
    train_idx = idx[n_test:]

    model_cfg = cfg.get("model", {"type": "ridge", "alpha": 1.0})
    model_type = str(model_cfg.get("type", "ridge")).lower()

    if model_type == "huber":
        reg = HuberRegressor(
            epsilon=float(model_cfg.get("epsilon", 1.35)),
            alpha=float(model_cfg.get("alpha", 0.0001)),
            max_iter=int(model_cfg.get("max_iter", 500)),
        )
        reg_step = ("huber", reg)
    else:
        reg = Ridge(alpha=float(model_cfg.get("alpha", 1.0)), random_state=seed)
        reg_step = ("ridge", reg)

    model = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
            reg_step,
        ]
    )

    log(f"training_rows={len(train_idx)} source_test_rows={len(test_idx)} target_eval_rows={len(X_tgt)}")
    model.fit(X_src.iloc[train_idx], y_src[train_idx])

    y_src_pred = model.predict(X_src.iloc[test_idx])
    y_tgt_pred = model.predict(X_tgt)

    metrics = {
        "run_id": run_id,
        "created_utc": _utc_now_iso(),
        "dataset_label": cfg.get("dataset_label"),
        "pair": {"source": source, "target": target},
        "regime": regime,
        "label": {"column": label_col, "transform": label_transform, "proxy": True},
        "features": feature_cols,
        "model": model_cfg,
        "overlap": {
            "run_id": overlap.get("run_id"),
            "overlap_band": overlap.get("overlap_band"),
            "matched_source_n": int(len(src)),
            "matched_target_n": int(len(tgt)),
        },
        "eval": {
            "source_test": _evaluate(y_src[test_idx], y_src_pred),
            "target": _evaluate(y_tgt, y_tgt_pred),
            "target_r2_bootstrap": _bootstrap_r2(y_tgt, y_tgt_pred, n_boot=n_boot, seed=seed),
        },
        "limitations": [
            "Label is a local proxy (value_memused_max) from job_partials, not the authoritative v3 peak_memory_fraction target.",
            "Model uses the feature set specified in the run config; treat this as an ablation baseline, not the final intended Phase 3 feature set.",
        ],
    }

    (exp_dir / "results" / "metrics.json").write_text(
        json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8"
    )

    # Save predictions
    src_pred_df = pd.DataFrame(
        {
            "jid": src.iloc[test_idx]["jid"].astype("string").to_numpy(),
            "y_true_log": y_src[test_idx],
            "y_pred_log": y_src_pred,
        }
    )
    tgt_pred_df = pd.DataFrame(
        {
            "jid": tgt["jid"].astype("string").to_numpy(),
            "y_true_log": y_tgt,
            "y_pred_log": y_tgt_pred,
        }
    )
    src_pred_df.to_parquet(exp_dir / "results" / "predictions_source_test.parquet", index=False)
    tgt_pred_df.to_parquet(exp_dir / "results" / "predictions_target.parquet", index=False)

    # Provenance
    meta = {
        "run_id": run_id,
        "created_utc": _utc_now_iso(),
        "script": str((repo_root / "scripts" / "model_transfer.py").resolve()),
        "config": str(cfg_path),
        "git": _git_info(repo_root.parents[1]),
        "python": sys.version.replace("\n", " "),
        "cwd": os.getcwd(),
    }
    (exp_dir / "manifests" / "run_metadata.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8"
    )

    used_files = []
    for p in src_used:
        used_files.append({"cluster": source, "path": str(p), "bytes": p.stat().st_size, "sha256": _sha256(p)})
    for p in tgt_used:
        used_files.append({"cluster": target, "path": str(p), "bytes": p.stat().st_size, "sha256": _sha256(p)})
    # include overlap index artifacts
    for p in [matched_source_idx, matched_target_idx]:
        used_files.append({"cluster": "overlap", "path": str(p), "bytes": p.stat().st_size, "sha256": _sha256(p)})

    (exp_dir / "manifests" / "input_files_used.json").write_text(
        json.dumps(used_files, indent=2, sort_keys=True), encoding="utf-8"
    )

    (exp_dir / "validation" / "python_version.txt").write_text(
        sys.version.replace("\n", " ") + "\n", encoding="utf-8"
    )
    try:
        rc, out, err = _run([sys.executable, "-m", "pip", "freeze"], repo_root)
        (exp_dir / "validation" / "pip_freeze.txt").write_text(
            out if rc == 0 else (out + "\n" + err), encoding="utf-8"
        )
    except Exception as e:
        (exp_dir / "validation" / "pip_freeze.txt").write_text(
            f"pip freeze failed: {e}\n", encoding="utf-8"
        )

    log("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

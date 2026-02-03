#!/usr/bin/env python3
"""Phase 2: overlap-aware regime matching (local proxy).

Builds matched cohorts for source vs target clusters by training a domain
classifier (propensity model) on a chosen feature set and selecting samples
with P(domain=source|x) within an overlap band.

Writes:
- results/overlap_report.json (coverage + AUC)
- results/matched_indices.parquet (jid + cluster + propensity + in_overlap)
- manifests/run_metadata.json + input_files_used.json
- validation/python_version.txt + pip_freeze.txt

NOTE: This implementation operates on local parquet files (e.g., EXP-001
job_partials) referenced by an input manifest.
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
from scipy.stats import ks_2samp
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
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


def _load_manifest_paths(manifest_path: Path, cluster: str) -> list[dict]:
    rows = json.loads(manifest_path.read_text(encoding="utf-8"))
    return [r for r in rows if r.get("cluster") == cluster]


def _read_cluster_frame(
    manifest_rows: list[dict],
    columns: list[str],
    max_rows: int,
    seed: int,
) -> tuple[pd.DataFrame, list[Path]]:
    # Sample across files/row-groups until row budget met (avoids loading full files).
    rng = random.Random(seed)
    paths = [Path(r["path"]) for r in manifest_rows]
    rng.shuffle(paths)

    dfs: list[pd.DataFrame] = []
    used_paths: list[Path] = []
    n = 0

    for p in paths:
        if n >= max_rows:
            break

        pf = pq.ParquetFile(str(p))
        available = set(pf.schema_arrow.names)
        col_subset = [c for c in columns if c in available]

        # Shuffle row groups for a bit of representativeness but deterministic via seed.
        rgs = list(range(pf.num_row_groups))
        rng.shuffle(rgs)

        used_any = False
        for rg in rgs:
            if n >= max_rows:
                break
            tbl = pf.read_row_group(rg, columns=col_subset)
            df = tbl.to_pandas()

            # Ensure expected columns exist
            for c in columns:
                if c not in df.columns:
                    df[c] = np.nan

            remaining = max_rows - n
            if len(df) > remaining:
                df = df.sample(remaining, random_state=seed)

            dfs.append(df[columns])
            n += len(df)
            used_any = used_any or (len(df) > 0)

        if used_any:
            used_paths.append(p)

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

    return out[columns], used_paths


def _derive_cpu_standard(df: pd.DataFrame) -> pd.Series:
    # Local proxy: treat jobs with no recorded GPU usage as CPU.
    gpu_cnt = df.get("value_gpu_cnt")
    gpu_sum = df.get("value_gpu_sum")
    if gpu_cnt is None and gpu_sum is None:
        return pd.Series([True] * len(df))

    gpu_cnt = gpu_cnt.fillna(0)
    gpu_sum = gpu_sum.fillna(0)
    return (gpu_cnt <= 0) & (gpu_sum <= 0)


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

    log_path = exp_dir / "logs" / "regime_matching.log"

    def log(msg: str) -> None:
        line = f"[{_utc_now_iso()}] {msg}"
        print(line)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    seed = int(cfg.get("random_seed", 1337))
    random.seed(seed)
    np.random.seed(seed)

    source = cfg["source_cluster"]
    target = cfg["target_cluster"]
    feature_cols = list(cfg["feature_columns"])
    overlap_lo, overlap_hi = cfg.get("overlap_band", [0.2, 0.8])
    max_rows = int(cfg.get("max_rows_per_cluster", 200000))

    manifest_path = (repo_root / cfg["inputs_manifest"]).resolve()

    log(f"run_id={run_id}")
    log(f"config={cfg_path}")
    log(f"manifest={manifest_path}")
    log(f"source={source} target={target} regime={cfg.get('regime')}")
    log(f"features={feature_cols}")
    log(f"overlap_band=[{overlap_lo},{overlap_hi}] max_rows_per_cluster={max_rows}")

    src_rows = _load_manifest_paths(manifest_path, source)
    tgt_rows = _load_manifest_paths(manifest_path, target)
    if not src_rows:
        raise FileNotFoundError(f"No manifest entries for source cluster: {source}")
    if not tgt_rows:
        raise FileNotFoundError(f"No manifest entries for target cluster: {target}")

    # Read minimal columns needed: jid + features
    needed = ["jid"] + sorted(set(feature_cols + ["value_gpu_cnt", "value_gpu_sum"]))

    log("reading source parquet(s)...")
    src, src_used = _read_cluster_frame(src_rows, needed, max_rows=max_rows, seed=seed)
    log(f"source_rows_loaded={len(src)} source_files_used={len(src_used)}")

    log("reading target parquet(s)...")
    tgt, tgt_used = _read_cluster_frame(tgt_rows, needed, max_rows=max_rows, seed=seed + 1)
    log(f"target_rows_loaded={len(tgt)} target_files_used={len(tgt_used)}")

    # Regime filter
    regime = cfg.get("regime", "cpu_standard")
    if regime == "cpu_standard":
        src_mask = _derive_cpu_standard(src)
        tgt_mask = _derive_cpu_standard(tgt)
    else:
        src_mask = pd.Series([True] * len(src))
        tgt_mask = pd.Series([True] * len(tgt))

    src = src.loc[src_mask].copy()
    tgt = tgt.loc[tgt_mask].copy()
    log(f"source_rows_after_regime={len(src)} target_rows_after_regime={len(tgt)}")

    # Build modeling frame
    src["domain"] = 1
    tgt["domain"] = 0

    X = pd.concat([src, tgt], ignore_index=True)
    y = X.pop("domain").astype(int).to_numpy()

    # Keep jid for output
    jid = X["jid"].astype("string")
    X = X[feature_cols]

    numeric_features = feature_cols

    model = Pipeline(
        steps=[
            (
                "prep",
                ColumnTransformer(
                    transformers=[
                        (
                            "num",
                            Pipeline(
                                steps=[
                                    ("impute", SimpleImputer(strategy="median")),
                                    ("scale", StandardScaler()),
                                ]
                            ),
                            numeric_features,
                        )
                    ],
                    remainder="drop",
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    C=float(cfg.get("propensity_model", {}).get("C", 1.0)),
                    max_iter=int(cfg.get("propensity_model", {}).get("max_iter", 2000)),
                    class_weight=cfg.get("propensity_model", {}).get("class_weight", "balanced"),
                    solver="lbfgs",
                ),
            ),
        ]
    )

    log("training domain classifier...")
    model.fit(X, y)

    proba_src = model.predict_proba(X)[:, 1]
    auc = float(roc_auc_score(y, proba_src))

    in_overlap = (proba_src >= float(overlap_lo)) & (proba_src <= float(overlap_hi))

    is_source = y == 1
    is_target = y == 0
    n_source = int(is_source.sum())
    n_target = int(is_target.sum())
    n_source_overlap = int(in_overlap[is_source].sum())
    n_target_overlap = int(in_overlap[is_target].sum())

    # Coverage relative to target
    target_covered = float(n_target_overlap / n_target) if n_target > 0 else 0.0

    def _ks(a: pd.Series, b: pd.Series) -> float | None:
        a = pd.to_numeric(a, errors="coerce").dropna().to_numpy()
        b = pd.to_numeric(b, errors="coerce").dropna().to_numpy()
        if len(a) == 0 or len(b) == 0:
            return None
        return float(ks_2samp(a, b, alternative="two-sided", mode="asymp").statistic)

    ks_all = {f: _ks(src[f], tgt[f]) for f in feature_cols}
    # For overlap KS, use rows in overlap for each domain
    src_overlap_mask = pd.Series(in_overlap[is_source], index=src.index)
    tgt_overlap_mask = pd.Series(in_overlap[is_target], index=tgt.index)
    ks_overlap = {
        f: _ks(src.loc[src_overlap_mask, f], tgt.loc[tgt_overlap_mask, f]) for f in feature_cols
    }

    report = {
        "run_id": run_id,
        "created_utc": _utc_now_iso(),
        "dataset_label": cfg.get("dataset_label"),
        "source_cluster": source,
        "target_cluster": target,
        "regime": regime,
        "feature_columns": feature_cols,
        "overlap_band": [overlap_lo, overlap_hi],
        "n_source": n_source,
        "n_target": n_target,
        "n_source_overlap": n_source_overlap,
        "n_target_overlap": n_target_overlap,
        "target_overlap_coverage": target_covered,
        "domain_classifier_auc": auc,
        "ks_by_feature_all": ks_all,
        "ks_by_feature_overlap": ks_overlap,
        "notes": [
            "Propensity model trained on a sampled subset of rows from parquet files listed in the input manifest.",
            "Regime definition is a local proxy: cpu_standard := (value_gpu_cnt<=0 and value_gpu_sum<=0).",
        ],
    }

    (exp_dir / "results" / "overlap_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )

    out_df = pd.DataFrame(
        {
            "jid": jid,
            "cluster": np.where(is_source, source, target),
            "propensity_source": proba_src,
            "in_overlap": in_overlap,
        }
    )
    out_df.to_parquet(exp_dir / "results" / "matched_indices.parquet", index=False)

    # Convenience: split cohorts (for Phase 3 modeling)
    out_df.loc[is_source & in_overlap].to_parquet(
        exp_dir / "results" / "matched_source_indices.parquet", index=False
    )
    out_df.loc[is_target & in_overlap].to_parquet(
        exp_dir / "results" / "matched_target_indices.parquet", index=False
    )

    # Provenance
    meta = {
        "run_id": run_id,
        "created_utc": _utc_now_iso(),
        "script": str((repo_root / "scripts" / "regime_matching.py").resolve()),
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
        used_files.append(
            {
                "cluster": source,
                "path": str(p),
                "bytes": p.stat().st_size,
                "sha256": _sha256(p),
            }
        )
    for p in tgt_used:
        used_files.append(
            {
                "cluster": target,
                "path": str(p),
                "bytes": p.stat().st_size,
                "sha256": _sha256(p),
            }
        )

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

    log(f"AUC={auc:.4f} target_overlap_coverage={target_covered:.4f}")
    log("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

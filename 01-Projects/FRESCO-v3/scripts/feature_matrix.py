#!/usr/bin/env python3
"""Compute a per-cluster feature availability/missingness matrix.

This script is Phase 1 of the v3 plan: it scans a sample of parquet shards per
cluster and reports:
- column presence (union/intersection)
- dtype stability (per cluster)
- missingness rates per column per cluster

It is designed to be reproducibility/traceability friendly:
- reads a single config file
- writes run metadata + input file manifest with SHA256

NOTE: This implementation targets local parquet samples (e.g., EXP-001 job_partials)
when the full `/depot/.../chunks-v3/` dataset is not available locally.
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

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq


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


def _normalize_dtype(t: pa.DataType) -> str:
    # Stable, human-readable type string.
    try:
        return str(t)
    except Exception:
        return repr(t)


def _missingness_for_table(tbl: pa.Table) -> dict[str, float]:
    out: dict[str, float] = {}
    n = tbl.num_rows
    for name in tbl.column_names:
        col = tbl[name]
        nulls = pc.sum(pc.is_null(col)).as_py() if n > 0 else 0
        out[name] = float(nulls) / float(n) if n > 0 else 0.0
    return out


def _merge_missingness(acc: dict[str, list[float]], miss: dict[str, float]) -> None:
    for k, v in miss.items():
        acc.setdefault(k, []).append(v)


def _mean(xs: list[float]) -> float:
    return float(sum(xs) / len(xs)) if xs else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[1]  # ...\FRESCO-v3
    cfg_path = (repo_root / args.config).resolve()
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    run_id = cfg["run_id"]
    exp_dir = (repo_root / "experiments" / run_id).resolve()

    for d in ["logs", "results", "manifests", "validation"]:
        (exp_dir / d).mkdir(parents=True, exist_ok=True)

    log_path = exp_dir / "logs" / "feature_matrix.log"

    def log(msg: str) -> None:
        line = f"[{_utc_now_iso()}] {msg}"
        print(line)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    log(f"run_id={run_id}")
    log(f"config={cfg_path}")

    # Resolve inputs
    seed = int(cfg.get("random_seed", 1337))
    random.seed(seed)

    inputs = cfg["inputs"]
    selected_files: list[dict] = []

    for spec in inputs:
        cluster = spec["cluster"]
        glob_pat = spec["paths_glob"]
        sample_n = int(spec.get("sample_n_files", 20))

        paths = sorted(Path(repo_root, glob_pat).resolve().parent.glob(Path(glob_pat).name))
        if not paths:
            raise FileNotFoundError(f"No parquet files matched for {cluster}: {glob_pat}")

        if sample_n > 0 and len(paths) > sample_n:
            paths = random.sample(paths, sample_n)

        for p in paths:
            selected_files.append({"cluster": cluster, "path": str(p)})

        log(f"{cluster}: selected_files={len(paths)}")

    # Scan (two-pass):
    #  1) collect schema + dtype sets per cluster
    #  2) compute missingness over full sampled files, treating missing columns as 100% missing
    per_cluster_columns: dict[str, set[str]] = {}
    per_cluster_dtype: dict[str, dict[str, set[str]]] = {}

    file_columns: list[dict] = []  # {cluster, path, columns:set[str]}

    for rec in selected_files:
        cluster = rec["cluster"]
        p = Path(rec["path"])

        pf = pq.ParquetFile(str(p))
        schema = pf.schema_arrow
        cols = [f.name for f in schema]
        per_cluster_columns.setdefault(cluster, set()).update(cols)

        dtypes = per_cluster_dtype.setdefault(cluster, {})
        for f in schema:
            dtypes.setdefault(f.name, set()).add(_normalize_dtype(f.type))

        file_columns.append({"cluster": cluster, "path": str(p), "columns": set(cols)})

    clusters = [s["cluster"] for s in inputs]
    union_cols = set().union(*(per_cluster_columns.get(c, set()) for c in clusters))
    inter_cols = set(union_cols)
    for c in clusters:
        inter_cols &= per_cluster_columns.get(c, set())

    per_cluster_missingness_samples: dict[str, dict[str, list[float]]] = {}
    per_cluster_rows_scanned: dict[str, int] = {}

    for rec in file_columns:
        cluster = rec["cluster"]
        p = Path(rec["path"])
        cols_present: set[str] = rec["columns"]

        pf = pq.ParquetFile(str(p))
        tbl = pf.read()  # full file; sampled N files keeps this bounded
        per_cluster_rows_scanned[cluster] = per_cluster_rows_scanned.get(cluster, 0) + tbl.num_rows

        miss = _missingness_for_table(tbl)
        for col in union_cols:
            if col not in cols_present:
                miss[col] = 1.0

        per_cluster_missingness_samples.setdefault(cluster, {})
        _merge_missingness(per_cluster_missingness_samples[cluster], miss)

    # Aggregate missingness means
    per_cluster_missingness_mean: dict[str, dict[str, float]] = {}
    for c in clusters:
        per_cluster_missingness_mean[c] = {
            col: _mean(per_cluster_missingness_samples.get(c, {}).get(col, []))
            for col in sorted(union_cols)
        }

    cutoff = float(cfg.get("missingness_safe_cutoff", 0.0))
    safe_cols = [
        col
        for col in sorted(inter_cols)
        if all(per_cluster_missingness_mean[c].get(col, 1.0) <= cutoff for c in clusters)
    ]

    # Write results
    results = {
        "run_id": run_id,
        "created_utc": _utc_now_iso(),
        "dataset_label": cfg.get("dataset_label"),
        "random_seed": seed,
        "missingness_safe_cutoff": cutoff,
        "clusters": clusters,
        "rows_scanned": per_cluster_rows_scanned,
        "n_files": {c: sum(1 for r in selected_files if r["cluster"] == c) for c in clusters},
        "union_columns": sorted(union_cols),
        "intersection_columns": sorted(inter_cols),
        "safe_columns": safe_cols,
        "dtype_by_cluster": {
            c: {k: sorted(v) for k, v in per_cluster_dtype.get(c, {}).items()} for c in clusters
        },
        "missingness_mean_by_cluster": per_cluster_missingness_mean,
        "limitations": [
            "Missingness is computed over full sampled parquet files (sampling-based across files, not across the full dataset).",
            "This run uses local EXP-001 job_partials parquet outputs, not the full v3 dataset under /depot/...",
        ],
    }

    (exp_dir / "results" / "feature_matrix.json").write_text(
        json.dumps(results, indent=2, sort_keys=True), encoding="utf-8"
    )

    # Manifests + env capture
    meta = {
        "run_id": run_id,
        "created_utc": _utc_now_iso(),
        "script": str((repo_root / "scripts" / "feature_matrix.py").resolve()),
        "config": str(cfg_path),
        "git": _git_info(repo_root.parents[1]),  # git repo root is ...\ObsidianNotes\Main
        "python": sys.version.replace("\n", " "),
        "cwd": os.getcwd(),
    }
    (exp_dir / "manifests" / "run_metadata.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8"
    )

    input_manifest = []
    for r in selected_files:
        p = Path(r["path"])
        input_manifest.append(
            {
                "cluster": r["cluster"],
                "path": str(p),
                "bytes": p.stat().st_size,
                "sha256": _sha256(p),
            }
        )
    (exp_dir / "manifests" / "input_files.json").write_text(
        json.dumps(input_manifest, indent=2, sort_keys=True), encoding="utf-8"
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

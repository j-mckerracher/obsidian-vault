# FRESCO v3 Schema & Provenance

**Last Updated**: 2026-02-03

## Purpose
Define the v3 canonical schema, dtype rules, and provenance fields required for:
- stable parquet output
- cross-cluster comparability
- publication-quality traceability

## Current implementation status (PROD-20260203-v3)
The current production artifact (`/depot/<group>/data/josh/FRESCO/chunks-v3/PROD-20260203-v3_v3.parquet`) does **not** yet fully realize the canonical schema below.

- Present in the current output: raw FRESCO-style fields such as `value_memused`, `value_gpu`, `value_cpuuser`, `queue`, `time`, and the provenance fields added by the pipeline.
- Not yet materialized in the current output: `runtime_sec`, `queue_time_sec`, `runtime_fraction`, `peak_memory_gb`, `node_memory_gb`, `peak_memory_fraction`, `partition`, `node_type`, `node_cores`, `gpu_count_per_node`, `gpu_model`, `memory_original_value`, `memory_original_unit`.

Treat the schema below as the **target canonical schema**. Current analysis must either derive the missing fields post hoc or extend the production build to emit them directly.

## 1. Canonical columns (minimum)
At minimum, v3 must contain:

### Identifiers
- `jid` (string/int, normalized to string)
- `jid_global` (string)
- `cluster` (categorical: anvil|conte|stampede)

### Allocations
- `nhosts` (int64)
- `ncores` (int64)
- `timelimit_sec` (float64)
- `timelimit_original` (float64 where possible)
- `timelimit_unit_original` (string)

### Timing (normalized)
- `submit_time`, `start_time`, `end_time` (timestamp)
- `runtime_sec`, `queue_time_sec`, `runtime_fraction`

### Memory (comparability)
- `peak_memory_gb` (float64, if available)
- `node_memory_gb` (float64)
- `peak_memory_fraction` (float64)

### Workload / hardware context
- `partition` (string)
- `node_type` (string)
- `node_cores` (int64)
- `gpu_count_per_node` (int64)
- `gpu_model` (string)

### Provenance: measurement semantics
- `memory_includes_cache` (bool)
- `memory_collection_method` (string)
- `memory_aggregation` (string)
- `memory_sampling_interval_sec` (float64)
- `memory_original_value` (float64)
- `memory_original_unit` (string)

## 2. Dtype stability rules
- No parquet writes with object columns when numeric is intended.
- Enforce explicit casts in extractors before write.
- If a column is missing for a cluster, it must exist with nulls (schema union by name).

## 3. Required provenance for cross-cluster claims
Any analysis intended as “cross-cluster insight” must be able to filter/stratify by:
- `cluster`
- `node_type` / taxonomy
- `memory_includes_cache` / `memory_collection_method`

## 4. Versioning
- Every output file must contain a dataset version string stored in run metadata.
- Run metadata must include git commit hashes and config.

---
name: canonical-schema
description: FRESCO v3 canonical column schema, required dtypes, and known per-cluster dtype drift. Use when writing extractors, validating output parquet files, adding new columns, or checking schema conformance.
---

Use this skill when writing extractors, checking output parquet files, or adding new columns. Every v3 output shard must conform to this schema.

## Required columns

### Identifiers
| Column | Type | Notes |
|---|---|---|
| `jid` | string | Normalized to string across all clusters |
| `jid_global` | string | Globally unique job ID |
| `cluster` | categorical | Must be one of `{anvil, conte, stampede}` |

### Allocations
| Column | Type |
|---|---|
| `nhosts` | int64 |
| `ncores` | int64 |
| `timelimit_sec` | float64 |
| `timelimit_original` | float64 |
| `timelimit_unit_original` | string |

### Timing
| Column | Type |
|---|---|
| `submit_time` | timestamp (UTC) |
| `start_time` | timestamp (UTC) |
| `end_time` | timestamp (UTC) |
| `runtime_sec` | float64 |
| `queue_time_sec` | float64 |
| `runtime_fraction` | float64 |

### Memory
| Column | Type | Notes |
|---|---|---|
| `peak_memory_gb` | float64 | May be null if not collected |
| `node_memory_gb` | float64 | From hardware metadata |
| `peak_memory_fraction` | float64 | `peak_memory_gb / node_memory_gb` |

### Workload / hardware context
| Column | Type |
|---|---|
| `partition` | string |
| `node_type` | string |
| `node_cores` | int64 |
| `gpu_count_per_node` | int64 |
| `gpu_model` | string |

### Provenance (measurement semantics)
| Column | Type | Purpose |
|---|---|---|
| `memory_includes_cache` | bool | True if memory metric includes disk cache |
| `memory_collection_method` | string | e.g., `procfs`, `cgroup`, `scheduler` |
| `memory_aggregation` | string | e.g., `max`, `mean` |
| `memory_sampling_interval_sec` | float64 | How often memory was sampled |
| `memory_original_value` | float64 | Raw value before normalization |
| `memory_original_unit` | string | e.g., `KB`, `MB`, `GB` |

## Dtype drift: known per-cluster issues

| Column | Anvil | Conte | Stampede | Fix |
|---|---|---|---|---|
| `ncores` | int64 | double | int32 | Cast to int64 |
| `nhosts` | int64 | double | int32 | Cast to int64 |
| timestamps | `timestamp[ns, UTC]` | `timestamp[ns, UTC]` | `timestamp[us, UTC]` | Normalize to ns |
| `exitcode` | string | string | dict-encoded string | Decode to string |
| `timelimit` | double | double | int64 | Cast to float64 |

## Rules for extractor authors

1. **Always cast explicitly** — never rely on pandas/pyarrow to infer dtypes during parquet write.
2. **Missing columns must be present as nulls** — use schema union-by-name; do not drop columns that are absent for one cluster.
3. **No object-dtype columns** in parquet output — convert to string or numeric before write.
4. **`cluster` must be populated** for every row — never leave it null.
5. **Timestamps must be timezone-aware** — normalize to UTC before write.

## Versioning

Any addition of new canonical columns requires a schema version bump in `run_metadata.json`. Existing columns must remain backward-compatible (rename = breaking change; add nullable column = non-breaking).

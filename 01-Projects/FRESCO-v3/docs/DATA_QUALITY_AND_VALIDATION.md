# FRESCO v3 Data Quality & Validation

**Last Updated**: 2026-02-03

## Implementation status (PROD-20260203-v3)
The current `build_production_v3.py` implementation writes **only** `validation/schema_report.json`.

The other artifacts required by this document —
- `validation/dtype_report.json`
- `validation/missingness_report.json`
- `validation/sanity_checks.json`

— are still part of the target validation spec and have **not** yet been implemented/generated for `PROD-20260203-v3`.

## 1. Validation levels

### Level 0 (Schema)
- Column set matches canonical schema
- Dtypes match expected types

### Level 1 (Sanity)
- Non-negative constraints: `nhosts>0`, `ncores>0`, `timelimit_sec>0`
- `runtime_sec >= 0`, `queue_time_sec >= 0`
- `peak_memory_fraction` in (0, 2] after cleaning (document thresholds)

### Level 2 (Cross-field consistency)
- `runtime_sec <= timelimit_sec * (1+epsilon)` (allow for scheduler rounding)
- `runtime_fraction` in [0,1+epsilon]

### Level 3 (Distribution monitoring)
- Missingness per column per cluster
- Drift checks across months (basic alarms)

## 2. Known data caveats
- Conte: time ordering inconsistencies in legacy accounting data (expected warning)
- Cross-cluster: partition/node_type may be disjoint; comparisons require regime matching

## 3. Required validation artifacts
Each run must produce machine-readable outputs:
- schema diff report
- dtype report
- missingness report (per cluster, per month)
- summary statistics table

## 4. Acceptance criteria for production
- Level 0 and Level 1 must pass
- Level 2 failures must be quantified and documented
- Level 3 used for monitoring, not hard-fail (unless extreme)

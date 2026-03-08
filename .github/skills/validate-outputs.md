# Skill: Validate Pipeline Outputs

After the production pipeline runs, validation artifacts must be produced and checked before the run is considered complete.

## Required validation artifacts

| File | Contents |
|------|----------|
| `validation/schema_report.json` | Column names + dtypes per cluster, union vs intersection |
| `validation/missingness_report.json` | Per-column missingness % per cluster |
| `validation/dtype_report.json` | Dtype per column per cluster + any drift flags |
| `validation/sanity_checks.json` | Row counts, date range coverage, cluster distribution |

These are produced automatically by `build_production_v3.py` when `--config` includes `"write_validation_reports": true`.

## Stop conditions — abort the run if any of these occur

- Any **dtype mismatch** during parquet append or write
- **Schema drift** that is not handled by union-by-name (i.e., a column appears in some shards but not others and is not nulled out)
- **Validation Level 0 or 1 fails** (schema or dtype invariants violated)
- `cluster` column is missing or contains values outside `{anvil, conte, stampede}`

## Key invariants to check

1. All output parquet files contain the `cluster` column with values in `{anvil, conte, stampede}`.
2. No dtype instability: `ncores`, `nhosts`, `timelimit` must be cast to canonical types before write.
3. Missing columns must be present as nulls — not absent.
4. Timestamps must be normalized to a single timezone/resolution.

See `docs/SCHEMA_AND_PROVENANCE.md` and `docs/DATA_QUALITY_AND_VALIDATION.md` for full rules.

## Checking validation output

```bash
cat /depot/<group>/data/josh/FRESCO/chunks-v3/validation/schema_report.json | python -m json.tool
cat /depot/<group>/data/josh/FRESCO/chunks-v3/validation/missingness_report.json | python -m json.tool
```

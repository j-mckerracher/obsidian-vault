# Copilot instructions for FRESCO v3

## Project location
- FRESCO v3 lives under `01-Projects\FRESCO-v3\` in this repo. Run commands from that folder unless noted.

## Commands (confirmed)
- Production dataset build:
  - `python scripts\build_production_v3.py --config config\production_v3.json`
  - SLURM wrapper: `scripts\production_v3.slurm`
- Phase 1 feature availability:
  - `python scripts\feature_matrix.py --config experiments\EXP-016_feature_matrix\config\exp016_feature_matrix.json`
- Phase 2 regime matching:
  - `python scripts\regime_matching.py --config experiments\EXP-017_regime_matching\config\exp017_regime_matching.json`
- Phase 3 transfer modeling:
  - `python scripts\model_transfer.py --config experiments\EXP-019_modeling_alloc_only\config\exp019_modeling_alloc_only.json`
- EXP-015 baseline replay:
  - `python scripts\reproduce_exp015_baseline.py --config experiments\EXP-015_baseline\config\reproduce_exp015_baseline.json`

## Architecture (big picture)
- **Dataset production pipeline**: `scripts\build_production_v3.py` reads raw FRESCO shards and writes unified `chunks-v3/` parquet with canonical schema/provenance plus `manifests/` and `validation/` artifacts (see `docs/DATASET_PRODUCTION_SPEC.md` + `runbooks/PRODUCTION_RUNBOOK.md`).
- **Research workflow is phased**:
  - Phase 1 feature availability/missingness (`scripts\feature_matrix.py` → `experiments\EXP-016_feature_matrix`, summarized in `docs\feature_matrix.md`).
  - Phase 2 overlap-aware regime matching (`scripts\regime_matching.py` → `experiments\EXP-017_*`, summarized in `docs\regime_matching.md`).
  - Phase 3 transfer modeling (`scripts\model_transfer.py` → `experiments\EXP-019_*`).
- **Standard experiment layout**: each `experiments\EXP-XXX` run contains `config\`, `logs\`, `results\`, `manifests\`, `validation\` and scripts auto-populate run metadata and input file manifests.

## Key conventions
- **Run IDs**: production runs use `PROD-YYYYMMDD-<tag>`; experiments use `EXP-XXX` (docs/CONFIGURATION.md).
- **Reproducibility is mandatory**: capture git commit/status, config, manifests, and environment lock (runbooks + `AGENT_PROMPT.md`).
- **Canonical schema/dtypes**: enforce explicit casts and union-by-name; missing columns must be present as nulls; `cluster` is required and must be {anvil, conte, stampede} (docs/SCHEMA_AND_PROVENANCE.md).
- **Cross-cluster claims require regime matching + overlap reporting**; default overlap band is `[0.2, 0.8]` (docs/WORKLOAD_TAXONOMY_AND_MATCHING.md).
- **Phase 1 “safe feature” rule**: features must have 0% missingness across clusters to be used for cross-cluster modeling (docs/feature_matrix.md).
- **job_partials aggregation**: Phase 2/3 scripts collapse duplicate `jid` rows to job-level via numeric max (scripts/regime_matching.py, scripts/model_transfer.py).
- **Gilbreth SLURM conventions**: submit with `sbbest <slurm_script>`, request GPUs with `#SBATCH --gres=gpu:1`, and wait 10 minutes after submission before proceeding (`AGENT_PROMPT.md`).

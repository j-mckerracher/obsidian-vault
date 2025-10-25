---
project: ARL RL
tags: [project/arl-rl]
created: 2025-10-03
---

# Experiments — ARL RL

Use this hub to track all changes we make, what results we observe, and relevant metadata for reproducibility (commit, seed, resources, paths).

## Summary table

| Date/Time (UTC) | Run ID | Commit | Param changes vs baseline | 100-ep Win Rate | Artifacts Path | Notes |
|---|---|---|---|---|---|---|
| 2025-10-04 01:39 | [[20251004_013929_baseline]] | (not tracked) | Batch 8, Mem 5k, Res 32x32, Eps 0.9/50k, TUF 100 | 8.00% | `/home/jmckerra/ARL-RL/runs/20251004_013929_baseline` | Memory-constrained baseline, NVIDIA A30 |
| 2025-10-04 23:30 | [[20251004_223122_sweepA_lr_0p00005]] | (not tracked) | Sweep A: LR=5e-5, Decay=50000, TUF=100 | 57.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251004_223122_sweepA_lr_0p00005` | Sweep A — LR |
| 2025-10-05 00:22 | [[20251004_233022_sweepA_lr_0p0001]] | (not tracked) | Sweep A: LR=1e-4, Decay=50000, TUF=100 | 6.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251004_233022_sweepA_lr_0p0001` | Sweep A — LR |
| 2025-10-05 01:17 | [[20251005_002239_sweepA_lr_0p00025]] | (not tracked) | Sweep A: LR=2.5e-4, Decay=50000, TUF=100 | 11.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251005_002239_sweepA_lr_0p00025` | Sweep A — LR |
| 2025-10-05 02:35 | [[20251005_014154_sweepB_decay_20000]] | (not tracked) | Sweep B: LR=1e-4, Decay=20000, TUF=100 | 13.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251005_014154_sweepB_decay_20000` | Sweep B — Decay |
| 2025-10-05 03:30 | [[20251005_023546_sweepB_decay_50000]] | (not tracked) | Sweep B: LR=1e-4, Decay=50000, TUF=100 | 1.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251005_023546_sweepB_decay_50000` | Sweep B — Decay |
| 2025-10-05 04:27 | [[20251005_033032_sweepB_decay_100000]] | (not tracked) | Sweep B: LR=1e-4, Decay=100000, TUF=100 | 10.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251005_033032_sweepB_decay_100000` | Sweep B — Decay |
| 2025-10-05 06:08 | [[20251005_050913_sweepC_tuf_50]] | (not tracked) | Sweep C: LR=1e-4, Decay=50000, TUF=50 | 2.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251005_050913_sweepC_tuf_50` | Sweep C — TUF |
| 2025-10-05 07:05 | [[20251005_060804_sweepC_tuf_100]] | (not tracked) | Sweep C: LR=1e-4, Decay=50000, TUF=100 | 9.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251005_060804_sweepC_tuf_100` | Sweep C — TUF |
| 2025-10-05 08:05 | [[20251005_070524_sweepC_tuf_200]] | (not tracked) | Sweep C: LR=1e-4, Decay=50000, TUF=200 | 53.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251005_070524_sweepC_tuf_200` | Sweep C — TUF |
| 2025-10-05 16:23 | [[20251005_161708_confirm_best_seed4]] | (not tracked) | Confirm: LR=5e-5, Decay=20000, TUF=200 (seed 4) | 37.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251005_161708_confirm_best_seed4` | Confirm — best params |
| 2025-10-05 16:29 | [[20251005_162324_confirm_best_seed6]] | (not tracked) | Confirm: LR=5e-5, Decay=20000, TUF=200 (seed 6) | 29.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251005_162324_confirm_best_seed6` | Confirm — best params |
| 2025-10-05 19:08 | [[20251005_165549_confirm_best_seed8]] | (not tracked) | Confirm: LR=5e-5, Decay=20000, TUF=200 (seed 8) | 7.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced//20251005_165549_confirm_best_seed8` | Confirm — best params |

|| 2025-10-19 03:48 | [[20251019_033706_E1_seed4]] | (not tracked) | Stage E1 (E1 recipe, 300 eps smoke): LR=5e-5, Decay=100k, TUF=300 | 80.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251019_033706_E1_seed4` | Smoke run — seed 4 (300 eps) |
||| 2025-10-19 15:12 | [[20251019_151225_E1_seed8]] | (not tracked) | Stage E1 (E1 recipe, 300 eps smoke): LR=5e-5, Decay=100k, TUF=300 | 20.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251019_151225_E1_seed8` | Smoke run — seed 8 (300 eps) |
|| 2025-10-21 17:12 | [[20251021_164433_E1_seed4]] | (not tracked) | E1: 800 eps @32×32; LR=5e-5, Decay=100k, TUF=300, Batch=4, StepMul=16 | 20.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251021_164433_E1_seed4` | 2h standby chunk |
|| 2025-10-21 17:15 | [[20251021_164432_E1_seed6]] | (not tracked) | E1: 800 eps @32×32; LR=5e-5, Decay=100k, TUF=300, Batch=4, StepMul=16 | 40.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251021_164432_E1_seed6` | 2h standby chunk |
|| 2025-10-21 17:24 | [[20251021_164435_E1_seed8]] | (not tracked) | E1: 800 eps @32×32; LR=5e-5, Decay=100k, TUF=300, Batch=4, StepMul=16 | 20.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251021_164435_E1_seed8` | 2h standby chunk |
|| 2025-10-21 21:30 | [[20251021_212042_E1_seed4]] | (not tracked) | E1 top-up: +200 eps @32×32; LR=5e-5, Decay=100k, TUF=300, Batch=4, StepMul=16 | 59.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251021_212042_E1_seed4` | 100-ep test |
|| 2025-10-21 21:41 | [[20251021_212805_E1_seed8]] | (not tracked) | E1 top-up: +200 eps @32×32; LR=5e-5, Decay=100k, TUF=300, Batch=4, StepMul=16 | 73.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251021_212805_E1_seed8` | 100-ep test |
|| 2025-10-21 21:42 | [[20251021_212805_E1_seed6]] | (not tracked) | E1 top-up: +200 eps @32×32; LR=5e-5, Decay=100k, TUF=300, Batch=4, StepMul=16 | 0.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251021_212805_E1_seed6` | 100-ep test |
|| 2025-10-19 15:12 | [[20251019_151225_E1_seed8]] | (not tracked) | Stage E1 (E1 recipe, 300 eps smoke): LR=5e-5, Decay=100k, TUF=300 | 20.00% | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251019_151225_E1_seed8` | Smoke run — seed 8 (300 eps) |

## Aggregated results (2025-10-21)
- Seeds: 4=59.0%, 6=0.0%, 8=73.0% (100-ep tests after top-ups)
- Mean: 44.0%; StdDev: 38.7 pp
- Decision (per criteria): Proceed to E2 (mean ≥ 40% and StdDev < 40 pp)

**Stage E1 1k-Episode Runs (Normal QoS - 2025-10-21, active)**
- Job IDs: 9795192 (seed 4), 9795193 (seed 6), 9795194 (seed 8)
- QoS: normal (higher priority, independent runs, no dependency chain)
- Submitted: 2025-10-21 04:29 UTC
- Configuration: 1,000 episodes per seed, 32×32 resolution, 4h wall time, Stage E1 recipe (Double DQN + LR scheduling)
- Expected start: within hours (normal QoS)
- Monitoring: `squeue -j 9795192,9795193,9795194`; results will aggregate in `e1_results.csv`
- Note: Replaced canceled standby chain (9774460–9774462, 2+ day queue) for faster execution

**Stage E1 1k-Episode Runs (Standby QoS - 2025-10-19, canceled)**  
- ~~Job chain: 9774460 (seed 4) → 9774461 (seed 6) → 9774462 (seed 8)~~
- ~~Submitted: 2h standby chunks with dependencies~~
- **Canceled 2025-10-21 due to long queue wait (2+ days); replaced with normal QoS jobs**

Tip: For each run, create a dedicated page in `Experiments/` from the template below and link it here.

## Plan

See [[Experiments/Plan|Experiments Plan]].

## How we track

- Only parameter changes (no algorithm edits) for win-rate improvement in Part 1
- Minimal targeted code changes for fixing NO_OP/attack behavior in Part 2
- Each run records:
  - Exact Config deltas (from baseline)
  - Git commit hash and branch
  - Random seed(s)
  - HPC resources (partition, GPU model, SLURM job ID) if applicable
  - Commands/env overrides used
  - Paths to logs, metrics, checkpoints, and plots
  - 100-episode test results and key training metrics
  - Observations and next steps

## Per-run pages

Create a new page under `Experiments/` from `Experiments/TEMPLATE` and add its link to the table above.

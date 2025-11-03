---
title: "Experiments — ARL RL"
last_updated: "2025-10-25T16:44:16Z"
tags: ["project/arl-rl", "experiments-index"]
---

# Experiments — ARL RL

Canonical hub tracking all experiments, results, and reproductibility metadata. Experiments are stored as canonical notes under `Documents/Experiments/` with detailed YAML and structured sections.

## Key Experiments (Canonical)

| ID | Date | Stage | Title | Algo | Params | Seeds | Episodes | Mean Win Rate | Status | Link |
|---|---|---|---|---|---|---|---|---|---|---|
| expt-20251025-e2-prod-3k | 2025-10-25 | E2 | Production — 3k Validation | Dueling DQN | LR=5e-5, TUF=400, Batch=4 | 4,6,8 | 3000 | **94.3%** ✓ | completed | [[expt-20251025-e2-prod-3k]] |
| expt-20251025-e2-confirm-1k | 2025-10-25 | E2 | Confirmation — 1k Runs | Dueling DQN | LR=5e-5, TUF=400, Batch=4 | 4,6,8 | 1000 | 91.3% | completed | [[expt-20251025-e2-confirm-1k]] |
| expt-20251025-e2-tuf-sweep | 2025-10-25 | E2 | TUF Sweep — 500ep Gate | Dueling DQN | LR=5e-5, TUF=400, Batch=4 | 4,6,8 | 500 | 52.7% | completed | [[expt-20251025-e2-tuf-sweep]] |
| expt-20251025-e3-per-smoke | 2025-10-25 | E3 | PER Smoke (α=0.6) | DQN+PER | LR=5e-5, α=0.6, TUF=400 | 4,6,8 | 500 | <E2 baseline | completed | [[expt-20251025-e3-per-smoke]] |
| expt-20251025-e3-per-sweep | 2025-10-25 | E3 | PER Alpha Sweep | DQN+PER | LR=5e-5, α∈{0.4,0.5}, TUF=400 | 4,6,8 | 300-500 | <E2 baseline | completed | [[expt-20251025-e3-per-sweep]] |

## Legacy Experiments Summary

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
|| 2025-10-25 | [[20251025_E2_TUF_sweep_alt3]] | (not tracked) | E2 TUF-sweep-alt-3: Dueling DQN, TUF=400, 500 eps (seeds 4,6,8) | 52.7% (mean) | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/TUF-sweep-alt-3/` | E2 gate passed |
|| 2025-10-25 | [[20251025_E2_run6_confirm_1k]] | (not tracked) | E2 run-6: 1k-ep confirmatory, Dueling DQN, TUF=400 (seeds 4,6,8) | 91.3% (mean) | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/run-6/` | **E2 CONFIRMED** |
|| 2025-10-25 | [[20251025_E3_PER_smoke]] | (not tracked) | E3 PER smoke: α=0.6, β=0.4→1.0, 500 eps (seeds 4,6,8) | Mixed (below E2) | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/E3-smoke/` | Seed 8 unstable |
|| 2025-10-25 | [[20251025_E3_PER_run2_alpha_sweep]] | (not tracked) | E3 PER run-2: α∈{0.4,0.5}, β=0.6→1.0 sweep (seeds 4,6,8) | Below E2 baseline | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/run-2/` | **PER parked** |
|| 2025-10-25 | [[20251025_E2_production_3k]] | (not tracked) | E2 production: 3k eps, frozen config (seeds 4,6,8) | **94.3% (mean)** | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251025_021201_E1_seed{4,6,8}/` | **E2 at scale** |

## Aggregated results

**Stage E1 Final (2025-10-21)**
- Seeds: 4=59.0%, 6=0.0%, 8=73.0% (100-ep tests after top-ups)
- Mean: 44.0%; StdDev: 38.7 pp
- Decision: Proceed to E2 (gate passed: mean ≥ 40% and StdDev < 40 pp)

**Stage E2 Confirmation (2025-10-25)**
- TUF-sweep-alt-3 (500 eps): Seeds 4=56.0%, 6=68.0%, 8=34.0% → Mean=52.7%, StdDev=35.9 pp (gate passed)
- run-6 (1k eps): Seeds 4=92.0%, 6=95.0%, 8=87.0% → Mean=91.3%, StdDev=4.0 pp
- **Production (3k eps)**: Seeds 4=97.0%, 6=88.0%, 8=98.0% → **Mean=94.3%, StdDev=5.7 pp**
- **E2 VALIDATED AT SCALE**: Frozen configuration performs excellently at 3k episodes (Dueling DQN, TUF=400, LR=5e-5, Decay=100k, Batch=4, Replay=100k, Res=32, StepMul=16)

**Stage E3 PER Exploration (2025-10-25)**
- Smoke (α=0.6, β=0.4→1.0): Mixed results, seed 8 unstable, below E2 baseline
- Alpha sweep (α=0.4,0.5, β=0.6→1.0): All configurations below E2 baseline
- **Decision: Park PER** — does not improve over E2; proceed with E2 production runs

Tip: For each run, create a dedicated page in `Experiments/` from the template below and link it here.

## Plan

See [[01 Projects/ARL-RL/Experiments/Plan|Experiments Plan]].

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

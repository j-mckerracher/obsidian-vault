---
title: "E2 Confirmation — 1,000-Episode Runs"
experiment_id: "expt-20251025-e2-confirm-1k"
date: "2025-10-25"
last_updated: "2025-10-25T16:44:16Z"
status: "completed"
tags: ["project/arl-rl", "experiment", "e2", "dueling-dqn", "validation"]
stage: "E2"
algorithm: "Dueling Double DQN + Cosine LR Scheduler"
dataset: "SC2 FindAndDefeatZerglings"
params:
  LR: 5e-5
  EPS_DECAY: 100000
  BATCH_SIZE: 4
  REPLAY_MEMORY_SIZE: 100000
  TARGET_UPDATE_FREQ: 400
  SCREEN_RESOLUTION: 32
  MINIMAP_RESOLUTION: 32
  STEP_MUL: 16
  USE_DUELING_DQN: true
seeds: [4, 6, 8]
episodes: 1000
code_ref:
  repo: "C:\\Users\\jmckerra\\PycharmProjects\\ARL-RL"
  entrypoint: "training_split.py"
artifacts: "/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/run-6/"
job_ids: ["(HPC jobs, see Job-Submission-Commands)"]
metrics:
  primary:
    name: "100-episode test win rate"
    value: 91.3
    unit: "percent"
    seed_breakdown:
      seed_4: 92.0
      seed_6: 95.0
      seed_8: 87.0
    stdev: 4.0
seeds_detail:
  seed_4:
    win_rate: 92.0
    episodes: 1000
    checkpoint: "model_ep1000.pth"
  seed_6:
    win_rate: 95.0
    episodes: 1000
    checkpoint: "model_ep1000.pth"
  seed_8:
    win_rate: 87.0
    episodes: 1000
    checkpoint: "model_ep1000.pth"
hardware:
  gpu: 1
  gpu_model: "A30"
  cpu: 4
  ram_gb: 50
  partition: "a30"
sources:
  - "[[../../../Experiments|Experiments.md]] — Summary table"
  - "[[../../../Work Completed/2025-10-25 E2 dueling validation and config freeze]]"
related:
  - "[[expt-20251025-e2-tuf-sweep]] — 500-ep gate validation (52.7%)"
  - "[[expt-20251025-e2-prod-3k]] — Production 3k runs (94.3%)"
  - "[[../../../Decisions/E2 Config Freeze]] — Config frozen based on these results"
---

## Summary
E2 confirmed with excellent results: **91.3% mean win rate** (seeds 92%/95%/87%), very low variance (4.0 pp). This run validated E2 configuration as production-ready and led to configuration freeze decision.

## Goal
Confirm E2 (Dueling DQN) performance with 1,000 episodes per seed after gate-passing 500-episode smoke run.

## Setup (Hardware/Software)
- **Environment**: Gilbreth HPC, conda GPU env
- **GPU**: NVIDIA A30
- **Time**: ~4 hours per seed

## Procedure
1. Run 1,000 episodes with frozen E2 config (from TUF-sweep-alt-3)
2. Test every 100 episodes on 100-episode evaluation set
3. Aggregate final test results
4. Decision gate: If mean ≥ 85% and stdev < 10 pp, freeze config; else iterate

## Results
### Win Rates
- **Seed 4**: 92.0%
- **Seed 6**: 95.0%
- **Seed 8**: 87.0%
- **Mean**: 91.3%
- **StdDev**: 4.0 pp ✓ (excellent reproducibility)

## Analysis
- **Gate passed**: Mean 91.3% >> 44% threshold; stdev 4.0 pp << 40 pp limit
- **Excellent stability**: Low variance across all seeds indicates robust configuration
- **Best result**: Seed 6 (95%) — near-optimal for 32×32 resolution
- **Ready for scale**: Decision made to freeze config and test at scale (3k episodes)

## Next Steps
- Proceed to production runs (3k episodes) — **COMPLETED** (achieved 94.3% mean)
- Consider resolution scaling (64×64) for future improvements
- Archive strategic checkpoints

## Jobs
- [[../../Job-Submission-Commands/2025-10-25-expt-20251025-e2-confirm-1k]]

## Artifacts
- Artifacts root: `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/run-6/`

## Changelog
- 2025-10-25T16:44:16Z Created from template

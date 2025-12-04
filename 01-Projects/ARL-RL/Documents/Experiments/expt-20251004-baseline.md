---
title: "Baseline Run with Memory Constraints"
experiment_id: "expt-20251004-baseline"
date: "2025-10-04"
last_updated: "2025-11-30T12:00:00Z"
status: "completed"
tags: ["project/arl-rl", "experiment", "baseline"]
dataset: ""
algorithm: "DQN"
params:
  BATCH_SIZE: 8
  REPLAY_MEMORY_SIZE: 5000
  SCREEN_RESOLUTION: 32
  MINIMAP_RESOLUTION: 32
  NUM_EPISODES: 100
  START_EPISODE: 0
  EPS_START: 0.90
  EPS_END: 0.05
  EPS_DECAY: 50000
  LEARNING_RATE: 0.0001
  TARGET_UPDATE_FREQ: 100
  STEP_MUL: 8
seeds: [4]
code_ref:
  repo: ""
  commit: ""
  entrypoint: "training_split.py"
artifacts: "/home/jmckerra/ARL-RL/runs/20251004_013929_baseline"
job_ids: []
metrics:
  primary: { name: "win_rate", value: 8.00, step: 100 }
  others:
    mean_reward: -0.43
hardware: { gpu: 1, cpu: 4, ram_gb: 24 } # CPU count assumed from typical SLURM config
sources: []
related: []
---
## Summary
First baseline run to establish performance with reduced GPU memory settings (32x32 resolution, smaller batch and replay memory).

## Goal
Establish a baseline win rate and verify memory optimization under memory-constrained settings.

## Setup (Hardware/Software)
- **Environment:** Gilbreth
- **Resources:** NVIDIA A30 24GB (used 23.2GB, 967MB free)
- **Code:** `training_split.py`

## Procedure
An interactive terminal session was used to run the experiment. Configuration was controlled via environment variables.

## Results
- **100-episode test win rate:** 8.00%
- **Mean/median test reward:** -0.43
- **Training:** 100 episodes completed successfully
- **Checkpoints:** `model_ep100.pth` saved
- **GPU:** No OOM errors with reduced settings

## Analysis
- Memory optimization was successful, no CUDA OOM.
- Win rate (8%) was lower than expected (20%) due to:
  - Reduced spatial resolution (64x64 -> 32x32)
  - Smaller batch size
  - Different random seed
  - Training from scratch

## Issues
- High baseline GPU memory usage (23.2GB/24GB) from other processes, indicating memory contention.

## Next Steps
- Try higher resolution (48x48 or 64x64) if memory allows.
- Increase batch size gradually to find memory limit.
- Run longer training (1000+ episodes) for better evaluation.
- Parameter sweep targets: EPS_DECAY, LEARNING_RATE, BATCH_SIZE, TARGET_UPDATE_FREQ.

## Jobs
- [[01 Projects/ARL-RL/Job-Submission-Commands/2025-10-04-expt-20251004-baseline.md]] — status: succeeded

## Artifacts
- Path: `/home/jmckerra/ARL-RL/runs/20251004_013929_baseline`

## Links

## Changelog
- 2025-11-30T12:00:00Z Created from template, migrated from `20251004_013929_baseline.md`

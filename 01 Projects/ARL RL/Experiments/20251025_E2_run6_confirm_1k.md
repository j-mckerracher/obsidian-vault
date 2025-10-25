---
project: ARL RL
tags: [project/arl-rl, stage-e2, dueling-dqn, frozen-config]
created: 2025-10-25
---

# E2 run-6 — 1k-Episode Confirmatory Runs (E2 Success)

## Overview
- Run ID: run-6 (seeds 4, 6, 8)
- Objective: Confirm E2 performance with 1,000 episodes per seed
- Part: Stage E2 — Dueling DQN final validation

## Config deltas (from E1 baseline)
- DUELING_DQN: enabled
- TARGET_UPDATE_FREQ: 300 → 400
- NUM_EPISODES: 1000
- All parameters locked to frozen E2 configuration:
  - LR: 5e-5
  - EPS_DECAY: 100000
  - BATCH_SIZE: 4
  - REPLAY_MEMORY_SIZE: 100000
  - STEP_MUL: 16
  - SCREEN_RESOLUTION / MINIMAP_RESOLUTION: 32

## Metadata
- Date/Time (UTC): 2025-10-25
- Git commit: (not tracked)
- Branch: main
- Seed(s): 4, 6, 8
- Environment: Gilbreth HPC
- SLURM: account=sbagchi, partition=a30, QoS=normal
- Resources: 1 GPU A30, 4 CPUs, 50GB RAM per job, 4h wall time
- Command / Env overrides:
```bash
sbatch --account=sbagchi --partition=a30 --qos=normal --gres=gpu:1 \
  --ntasks=1 --cpus-per-task=4 --mem=50G --time=04:00:00 \
  --export=ALL,RL_SEED=<seed>,RL_NUM_EPISODES=1000,RL_LEARNING_RATE=0.00005,\
RL_EPS_DECAY=100000,RL_BATCH_SIZE=4,RL_REPLAY_MEMORY_SIZE=100000,\
RL_SCREEN_RESOLUTION=32,RL_STEP_MUL=16,RL_TARGET_UPDATE_FREQ=400,\
RL_DUELING_DQN=1 \
  scripts/run_e2.sh
```
- Artifacts path: `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/run-6/`

## Results
- 100-episode test win rates:
  - Seed 4: 92.0%
  - Seed 6: 95.0%
  - Seed 8: 87.0%
- Aggregate: Mean = 91.3%, StdDev = 4.0 pp
- **E2 CONFIRMED**: Excellent win rate with low variance
- Training curves: Strong convergence across all seeds
- Checkpoints: Final models saved

## Observations
- Outstanding performance: mean win rate 91.3% (far exceeding gate threshold)
- Very low variance (4.0 pp) indicates stable, reproducible training
- All three seeds performed strongly (87-95% range)
- Dueling DQN architecture clearly superior to E1 baseline
- Configuration ready for production use

## Next steps
- **Freeze E2 configuration** as production baseline
- Document frozen config in Decisions file
- Update Status, Plan, and Experiments hub
- Proceed to Stage E3 (PER) smoke tests with E2 as baseline
- Consider E2 production runs at 2k-4k episodes for extended validation

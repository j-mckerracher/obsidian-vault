---
project: ARL RL
tags: [project/arl-rl, stage-e2, dueling-dqn]
created: 2025-10-25
---

# E2 TUF-sweep-alt-3 — Dueling DQN Validation (500 episodes)

## Overview
- Run ID: TUF-sweep-alt-3 (seeds 4, 6, 8)
- Objective: Validate dueling DQN with TUF=400 at 500 episodes per seed
- Part: Stage E2 — Dueling DQN architecture

## Config deltas (from E1 baseline)
- DUELING_DQN: enabled
- TARGET_UPDATE_FREQ: 300 → 400
- NUM_EPISODES: 500
- All other parameters locked to E2 baseline:
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
- SLURM: account=sbagchi, partition=a30, QoS=standby
- Resources: 1 GPU A30, 4 CPUs, 50GB RAM per job
- Command / Env overrides:
```bash
sbatch --account=sbagchi --partition=a30 --qos=standby --gres=gpu:1 \
  --ntasks=1 --cpus-per-task=4 --mem=50G --time=02:00:00 \
  --export=ALL,RL_SEED=<seed>,RL_NUM_EPISODES=500,RL_LEARNING_RATE=0.00005,\
RL_EPS_DECAY=100000,RL_BATCH_SIZE=4,RL_REPLAY_MEMORY_SIZE=100000,\
RL_SCREEN_RESOLUTION=32,RL_STEP_MUL=16,RL_TARGET_UPDATE_FREQ=400,\
RL_DUELING_DQN=1 \
  scripts/run_e2.sh
```
- Artifacts path: `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/TUF-sweep-alt-3/`

## Results
- 100-episode test win rates:
  - Seed 4: 56.0%
  - Seed 6: 68.0%
  - Seed 8: 34.0%
- Aggregate: Mean = 52.7%, StdDev = 35.9 pp
- Gate criterion: **PASSED** (mean ≥ 44%, stdev < 40 pp)
- Training curves: Available in run directories
- Checkpoints: Saved at intervals

## Observations
- Dueling architecture showed promising results with TUF=400
- High variance across seeds but mean win rate exceeded E1 baseline
- Seed 8 lower than seeds 4/6 but still reasonable
- Gate criteria met, indicating readiness for 1k-episode confirmatory runs

## Next steps
- Proceed to 1,000-episode confirmatory runs (run-6) with locked parameters
- If confirmed, freeze E2 configuration as production baseline
- Prepare for Stage E3 (PER) smoke tests

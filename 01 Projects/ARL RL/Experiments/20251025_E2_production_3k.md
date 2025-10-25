---
project: ARL RL
tags: [project/arl-rl, stage-e2, dueling-dqn, production]
created: 2025-10-25
---

# E2 Production — 3,000-Episode Validation Runs

## Overview
- Run ID: E2 production 3k (seeds 4, 6, 8)
- Objective: Long-duration validation of frozen E2 configuration at scale
- Part: Stage E2 — Production validation

## Config deltas (from E1 baseline)
- DUELING_DQN: enabled
- TARGET_UPDATE_FREQ: 300 → 400
- NUM_EPISODES: 3000
- All parameters locked to frozen E2 configuration:
  - LR: 5e-5
  - EPS_DECAY: 100000
  - BATCH_SIZE: 4
  - REPLAY_MEMORY_SIZE: 100000
  - STEP_MUL: 16
  - SCREEN_RESOLUTION / MINIMAP_RESOLUTION: 32

## Metadata
- Date/Time (UTC): 2025-10-25 02:12
- Git commit: (not tracked)
- Branch: main
- Seed(s): 4, 6, 8
- Environment: Gilbreth HPC
- SLURM: account=sbagchi, partition=a30, QoS=normal
- Resources: 1 GPU A30, 4 CPUs, 50GB RAM per job
- Command / Env overrides:
```bash
sbatch --account=sbagchi --partition=a30 --qos=normal --gres=gpu:1 \
  --ntasks=1 --cpus-per-task=4 --mem=50G --time=06:00:00 \
  --export=ALL,RL_SEED=<seed>,RL_NUM_EPISODES=3000,RL_LEARNING_RATE=0.00005,\
RL_EPS_DECAY=100000,RL_BATCH_SIZE=4,RL_REPLAY_MEMORY_SIZE=100000,\
RL_SCREEN_RESOLUTION=32,RL_STEP_MUL=16,RL_TARGET_UPDATE_FREQ=400,\
RL_DUELING_DQN=1 \
  scripts/run_e2.sh
```
- Artifacts path (HPC): `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251025_021201_E1_seed4/`
- Artifacts path (local): `C:\Users\jmckerra\OneDrive - purdue.edu\Documents\ARL-RL-Experiment-Results\10-25-2025\`

## Results
- 100-episode test win rates:
  - Seed 4: **97.0%** (502.0 total reward, 5.02 avg)
  - Seed 6: **88.0%** (163.0 total reward, 1.63 avg)
  - Seed 8: **98.0%** (517.0 total reward, 5.17 avg)
- Aggregate: **Mean = 94.3%, StdDev = 5.7 pp**
- **E2 VALIDATED AT SCALE**: Performance improved vs. 1k runs (91.3% → 94.3%)
- Training curves: Stable convergence across all seeds
- Checkpoints: Saved every 100 episodes (ep100 through ep3000)

## Observations
- **Outstanding performance**: 94.3% mean win rate with low variance (5.7 pp)
- **Improved over 1k runs**: Mean increased from 91.3% to 94.3%
- All three seeds performed excellently (88-98% range)
- Seed 8 reached 98%, highest individual performance yet
- Longer training (3k vs 1k episodes) yielded better final policies
- Stable, reproducible training across all seeds
- Configuration robustly validated at production scale

## Checkpoints saved
Each seed has 30+ checkpoints:
- `model_ep100.pth` through `model_ep3000.pth` (every 100 episodes)
- File size: ~64MB per checkpoint
- **Recommendation**: Archive only strategic checkpoints (ep100, ep1000, ep2000, ep3000) to save space

## Next steps
- **Document** these results in Status/Plan/Experiments
- **Options for next stage**:
  1. Resolution scaling: Test 64×64 with frozen E2 config
  2. Stage E4: N-step returns (n=3) exploration
  3. Extended validation: 4k-5k episode runs for ultimate confidence
  4. Deployment: Use best checkpoint (seed 8 ep3000) for demos/production

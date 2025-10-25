---
project: ARL RL
tags: [project/arl-rl]
created: 2025-10-03
---

# TEMPLATE — Experiment Run

Fill this out for each run. Save the file as `Experiments/<run_id>.md` and link it in Experiments.md.

## Overview
- Run ID: <yyyyMMdd_HHmmss_runX or descriptive>
- Objective: what are we testing?
- Part: [1 = parameter-only | 2 = NO_OP fix validation]

## Config deltas (from baseline)
List only changed parameters, with previous -> new values.
- EPS_START: 
- EPS_DECAY: 
- EPS_END: 
- LEARNING_RATE: 
- BATCH_SIZE: 
- TARGET_UPDATE_FREQ: 
- REPLAY_MEMORY_SIZE: 
- STEP_MUL: 
- SCREEN_RESOLUTION / MINIMAP_RESOLUTION: 
- Reward shaping (PER_STEP, MOVE_CLOSER, etc.): 
- START_EPISODE / NUM_EPISODES: 
- SAVE_PATH (run subdir): 

## Metadata
- Date/Time (UTC): 
- Git commit: 
- Branch: 
- Seed(s): 
- Environment: [Local | Gilbreth]
- SLURM: [account, partition, job id, array id]
- Resources: [GPU model/count | CPU]
- Command / Env overrides: (copy exact command and RL_* env vars)
- Artifacts path: 

## Results
- 100-episode test win rate: 
- Mean/median test reward: 
- Training curves: [link or embedded]
- Checkpoints: [link]
- Sweep position (if any): 

## Observations
- What worked / didn’t?
- Signs of NO_OP / idle behavior?
- Unexpected behaviors or crashes?

## Next steps
- Immediate follow-ups:
- Longer-term ideas:

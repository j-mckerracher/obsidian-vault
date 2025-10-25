---
title: "E3 PER Smoke — Initial Testing (α=0.6)"
experiment_id: "expt-20251025-e3-per-smoke"
date: "2025-10-25"
last_updated: "2025-10-25T16:44:16Z"
status: "completed"
tags: ["project/arl-rl", "experiment", "e3", "per", "ablation"]
stage: "E3"
algorithm: "Dueling Double DQN + PER (Prioritized Experience Replay)"
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
  PER_ENABLED: true
  PER_ALPHA: 0.6
  PER_BETA_START: 0.4
  PER_BETA_END: 1.0
seeds: [4, 6, 8]
episodes: 500
code_ref:
  repo: "C:\\Users\\jmckerra\\PycharmProjects\\ARL-RL"
  entrypoint: "training_split.py"
artifacts: "/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/E3-smoke/"
job_ids: ["(HPC jobs, standby QoS)"]
metrics:
  primary:
    name: "100-episode test win rate"
    value: "mixed"
    seed_breakdown:
      seed_4: "60-70%"
      seed_6: "50-60%"
      seed_8: "10-15%"
  comparison_to_e2_baseline:
    e2_baseline_mean: 91.3
    e3_smoke_status: "below baseline"
hardware:
  gpu: 1
  gpu_model: "A30"
  cpu: 4
  ram_gb: 50
  partition: "a30"
sources:
  - "[[../../../Experiments|Experiments.md]]"
  - "[[../../../Work Completed/2025-10-25 E3 PER exploration and parking decision]]"
related:
  - "[[expt-20251025-e2-prod-3k]] — E2 baseline (94.3%)"
  - "[[expt-20251025-e3-per-sweep]] — Alpha sweep follow-up"
  - "[[../../../Decisions/2025-10-25 Park Stage E3 PER]] — Parking decision"
---

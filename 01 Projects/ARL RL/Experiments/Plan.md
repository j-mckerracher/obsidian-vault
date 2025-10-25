---
project: ARL RL
tags: [project/arl-rl]
created: 2025-10-04
---

# Experiments Plan — ARL RL

Objective: Improve win rate via parameter-only changes (Part 1), and validate NO_OP action-selection fix (Part 2), under memory constraints on Gilbreth.

Guiding principles
- Change 1–2 knobs per run to attribute impact clearly.
- Run long enough to get a meaningful signal (≥1500 episodes) for baselines; shorter (800–1200) for coarse sweeps.
- Keep batch small due to GPU contention; raise only if memory allows.
- Prefer 32×32 resolution under memory pressure; test 64×64 only if headroom is available.

Phases

Algorithmic upgrades plan (E1–E4)

Execution (current)
- Now running Stage E1 at 32×32 via `scripts/run_e1.sh` (seeds 4,6,8; 10k episodes; replay 100k; EPS_END=0.01; EPS_DECAY=100k; TUF=300; STEP_MUL=16; LR=5e-5).
- Use `scripts/wait_and_run_e1.sh` to automatically wait for GPU memory headroom, then launch E1.
- Results will be appended to `$RL_SAVE_PATH/e1_results.csv` and per-run pages will be created from run JSONs.
- E1: Double DQN + LR scheduler (cosine or step)
  - Double DQN target: select next best action/spatial via policy_net; evaluate that choice via target_net; use the max between non-spatial and spatial targets.
  - LR scheduler: CosineAnnealingLR (T_max=NUM_EPISODES, eta_min=MIN_LR) or StepLR (step_size, gamma).
  - Training recipe suggestion (32×32): NUM_EPISODES=10000, REPLAY_MEMORY_SIZE=100000, EPS_END=0.01, EPS_DECAY=100000, TARGET_UPDATE_FREQ=300, STEP_MUL=16, LR=5e-5.
- E2: Dueling for non-spatial head (V + A formulation)
- E3: Prioritized Experience Replay (PER) with α~0.6, β annealing 0.4→1.0
- E4: N-step returns (e.g., N_STEP=3)

Phase 0 — Establish baseline (single run)
- Purpose: a fair starting point before sweeping.
- Suggested parameters:
  - Episodes: RL_NUM_EPISODES=1500
  - Batch: RL_BATCH_SIZE=8 (16 if memory allows)
  - Resolution: 32×32 (switch to 64×64 only if headroom appears)
  - Replay buffer: RL_REPLAY_MEMORY_SIZE=50000
  - Epsilon: RL_EPS_START=0.90, RL_EPS_END=0.05, RL_EPS_DECAY=50000
  - Learning rate: RL_LEARNING_RATE=1e-4
  - Target update: RL_TARGET_UPDATE_FREQ=100
  - Other: RL_STEP_MUL=8, fixed RL_SEED
- Output: 100-episode test; record win rate and logs.

Phase 1 — Targeted sweeps (short runs, 800–1200 episodes)
- Sweep A: Learning rate [5e-5, 1e-4, 2.5e-4]
- Sweep B: Epsilon decay [20000, 50000, 100000] (use best LR)
- Sweep C: Target update frequency [50, 100, 200] (use best LR/decay)
- Fixed: Batch=8/16, Replay=50k, StepMul=8, Seed fixed, Resolution same as Phase 0.
- Output: Rank by test win rate; keep top 2 configs.

Phase 2 — Confirm and extend (per-config, 2 seeds)
- For each of the top 2:
  - Episodes: RL_NUM_EPISODES=3000
  - Seeds: two (e.g., 4 and 6)
- Output: Mean/variance of 100-episode test win rate; pick winner.

Phase 3 — Resolution bump (only if GPU headroom appears)
- Rerun Phase 2 winner at 64×64 with same seeds/episodes.
- Keep 64×64 only if it improves ≥ 5–10 pp.

Optional knobs (parameter-only)
- Replay size: try 100k if CPU RAM permits.
- Reward shaping: test RL_STEP_PENALTY=-0.0005, RL_MOVE_CLOSER_REWARD=0.1 (change one at a time).

What not to do now
- Don’t chase max batch size on a crowded GPU; diminishing returns.
- Don’t mix many knobs in one run.

Measurement protocol
- Always run a 100-episode test after training and record win rate and average reward.
- Capture env vars (RL_*, CUDA_*, PYTORCH_*, SC2PATH) for each run.
- Use RL_RUN_ID to make artifacts paths unique per run.

Notes for Part 2 (NO_OP fix validation)
- After selecting best Part 1 parameters, repeat Phase 2 with the NO_OP fix enabled and compare win rates.

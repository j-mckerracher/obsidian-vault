---
project: ARL RL
tags: [project/arl-rl, plan]
created: 2025-10-11
---

# Plan — ARL RL (Overarching)

## Objective
Improve SC2 FindAndDefeatZerglings win rate with a staged RL roadmap under HPC constraints (Gilbreth), while maintaining reproducible runs and robust infrastructure.

## Overarching Plan (hierarchy)

- Stage roadmap (algorithmic)
- E1 (current): Double DQN + LR scheduler
    - Prioritize short 2h standby chunks (~800–1200 eps/job) at 32×32; submit independent jobs per seed; resume until ≥1000 eps/seed
    - Harden training under mixed precision and memory constraints
    - HPC execution: normal QoS used opportunistically; heavy queue observed, so prefer standby backfill micro‑chunks
    - Evaluate win rates; decide go/no-go for E2
  - E2 (next): Dueling DQN (non-spatial head)
    - Integrate V/A decomposition; keep other hyperparams stable
    - Compare against E1 across 2–3 seeds
  - E3: Prioritized Experience Replay (PER)
    - α≈0.6, β annealing 0.4→1.0; measure sample efficiency
  - E4: N-step returns (e.g., n=3)
    - Tune n; assess stability and performance

- Parameter-only plan (completed/feeding into E1)
  - Phase 0: Baseline
  - Phase 1: Sweeps A–C (LR, decay, TUF)
  - Phase 2: Confirm and extend (multi-seed)
  - Phase 3: Resolution bump if headroom

- HPC execution plan (Gilbreth)
  - Partition/account/QoS: a30 / sbagchi / standby|normal
  - GPUs via `--gres=gpu:N`; typical resources: ntasks=1, cpus-per-task=4, mem=50G
- Short-window runs: chunk episodes (~800–1200 in 2h) on standby; submit independent (no dependencies) to maximize backfill; use arrays if helpful
  - Long-window runs: normal QoS (if permitted) with 12h for 4k/seed; due to queue pressure, only when reserved/priority is available
  - Environment: conda init without modules; activate env by path
  - Logging & artifacts: config.json + eval/test_results.json + CSV aggregation

## Current state
- 2h standby chunks completed for seeds 4/6/8 (~800 eps each): see [[Work Completed/2025-10-21 Stage E1 2h standby chunks 800eps seeds 4 6 8]]
- Normal QoS submissions are experiencing long waits; using standby micro‑chunks to progress
- Mixed-precision masking bug fixed (FP16 overflow → dtype-safe masking): [[Work Completed/2025-10-11 FP16 masking overflow fix]]
- SLURM integration complete; docs and wrapper in place
- Status: [[Status]]

## Next steps (roll-up)
- Submit additional 200–400 episode chunks per seed on standby to reach ≥1000 episodes/seed today
- If GPUs available, run jobs in parallel (independent submissions or arrays) to minimize wall time
- After ≥1000 eps/seed: aggregate results, update Experiments and Status, and decide:
  - Proceed to E2 (Dueling) if mean win rate acceptable and variance manageable
  - Otherwise, adjust E1 hyperparams (e.g., TUF from 300→200 or 400) and rerun short chunks
- Optional infrastructure: auto-resume from latest checkpoint; add deadline guard to save before SLURM timeout

## Links to detailed plans/sources
- Experiments Plan (detailed phases E1–E4): [[Experiments/Plan]]
- Execution & best practices: [[Documents/Submitting SLURM Jobs on Gilbreth for LLMs]], [[Notes/Engineering Notes - Mixed Precision and HPC]], [[Documents/Common Commands]]
- Decisions guiding the plan: [[Decisions/Index]]
- Experiments hub and results: [[Experiments]]
- Work in progress/completed: [[Work Completed/Index]]
- Open tasks: [[To Do]], [[Backlog]]

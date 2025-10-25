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

## Current state (2025-10-25)
- **Stage E2 confirmed**: Dueling DQN achieves 91.3% mean win rate (seeds 4/6/8: 92%/95%/87%) with 4.0 pp stdev
- **Stage E3 PER parked**: Tested α∈{0.4,0.5,0.6} with β annealing; all configs underperformed E2 baseline
- **Frozen E2 config**: LR=5e-5, EPS_DECAY=100k, Batch=4, Replay=100k, Res=32, StepMul=16, TUF=400, Dueling enabled
- SLURM integration complete; docs and wrapper in place
- Mixed-precision masking bug fixed (FP16 overflow → dtype-safe masking)
- Status: [[Status]]

## Next steps (roll-up)
- **E2 production runs**: Submit 2k-4k episode runs per seed (seeds 4, 6, 8) with frozen E2 config on normal QoS (sbagchi account)
- **Validation**: Aggregate results to confirm long-term stability and performance at scale
- **Post-production options**:
  - Resolution scaling: Test 64×64 if E2 production is stable
  - Stage E4: Design and test N-step returns (n=3) with E2 as baseline
  - Revisit PER after architecture/resolution changes if warranted
- **Infrastructure**: Optional auto-resume and deadline guards for long runs

## Links to detailed plans/sources
- Experiments Plan (detailed phases E1–E4): [[Experiments/Plan]]
- Execution & best practices: [[Documents/Submitting SLURM Jobs on Gilbreth for LLMs]], [[Notes/Engineering Notes - Mixed Precision and HPC]], [[Documents/Common Commands]]
- Decisions guiding the plan: [[Decisions/Index]]
- Experiments hub and results: [[Experiments]]
- Work in progress/completed: [[Work Completed/Index]]
- Open tasks: [[To Do]], [[Backlog]]

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
- **Stage E2 validated at scale**: 3k-episode production runs achieve 94.3% mean win rate (seeds 4/6/8: 97%/88%/98%) with 5.7 pp stdev
- **E2 progression**: 500 eps (52.7%) → 1k eps (91.3%) → 3k eps (94.3%) — robust scaling
- **Stage E3 PER parked**: Tested α∈{0.4,0.5,0.6} with β annealing; all configs underperformed E2 baseline
- **Frozen E2 config**: LR=5e-5, EPS_DECAY=100k, Batch=4, Replay=100k, Res=32, StepMul=16, TUF=400, Dueling enabled
- SLURM integration complete; docs and wrapper in place
- Mixed-precision masking bug fixed (FP16 overflow → dtype-safe masking)
- Status: [[Status]]

## Next steps (roll-up)
**E2 production complete (94.3% at 3k episodes). Choose next direction:**

1. **Resolution scaling (64×64)**: Test frozen E2 at higher res; 500-1k eps smoke per seed; ~4x resources
2. **Stage E4 (N-step returns)**: Add n=3 bootstrapping to E2; 500-1k eps smoke per seed; similar resources
3. **Extended validation**: Push E2 to 4k-5k episodes to test convergence limits
4. **Deployment prep**: Archive checkpoints, prepare best model (seed 8 ep3000) for demos/production

**Infrastructure improvements (optional)**:
- Auto-resume from checkpoint
- Deadline guards for SLURM timeouts
- Checkpoint cleanup scripts

## Links to detailed plans/sources
- Experiments Plan (detailed phases E1–E4): [[Experiments/Plan]]
- Execution & best practices: [[Documents/Submitting SLURM Jobs on Gilbreth for LLMs]], [[Notes/Engineering Notes - Mixed Precision and HPC]], [[Documents/Common Commands]]
- Decisions guiding the plan: [[Decisions/Index]]
- Experiments hub and results: [[Experiments]]
- Work in progress/completed: [[Work Completed/Index]]
- Open tasks: [[To Do]], [[Backlog]]

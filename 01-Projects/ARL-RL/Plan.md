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

## Milestones

| Milestone | Owner | Target Date | Status | Links |
|---|---|---|---|---|
| E1 Baseline (Double DQN + LR scheduler) | josh | 2025-10-21 | ✅ Done | [[Experiments#expt-20251025-e2-tuf-sweep]] |
| E2 Validation (Dueling DQN gate) | josh | 2025-10-25 | ✅ Done | [[Experiments#expt-20251025-e2-confirm-1k]] |
| E2 Production (3k episodes) | josh | 2025-10-25 | ✅ Done | [[Experiments#expt-20251025-e2-prod-3k]] (94.3%) |
| E3 PER Exploration (frozen E2) | josh | 2025-10-25 | ✅ Parked | [[2025-10-25 Park Stage E3 PER]] |
| Resolution Scaling (64×64) | josh | 2025-10-26 | 🔄 In Progress | [[Experiments]] — awaiting results |
| E4 N-step Returns (design) | josh | 2025-10-28 | ⏸ Blocked | Pending 64×64 results |
| Documentation Restructuring Phase 1 | josh | 2025-10-25 | ✅ Done | [[RESTRUCTURING_SUMMARY_2025-10-25]] |
| Documentation Phase 2 (legacy) | josh | 2025-10-26 | 🔄 In Progress | [[2025-10-25]] |

## Tasks

### In Progress
- Resolution scaling 64×64 smoke runs (E2 config, 500 eps per seed) — jobs queued on Gilbreth
- Phase 2 documentation consolidation (job notes, daily logs, legacy experiments)

### Backlog
- E4 N-step returns design and smoke tests
- Extended validation (4k-5k episodes)
- Checkpoint cleanup and deployment prep
- Obsidian dataview queries for experiment filtering
- KPI dashboard setup

### Done
- E1 baseline establishment and validation
- E2 implementation and production validation (94.3% mean)
- E3 PER exploration and parking decision
- Documentation Phase 1 (5 canonical experiments, standardized hub)

## Risks & Mitigation

| Risk | Impact | Mitigation | Status |
|---|---|---|---|
| 64×64 runs exceed memory | High | Use 80GB memory allocation; monitor GPU usage | ✅ Mitigated |
| E2 performance degrades with resolution | Medium | Have fallback to 48×48 or revert to 32×32 | ✅ Planned |
| PER fundamentally incompatible | Medium | Already explored and parked; focus on other improvements | ✅ Resolved |
| Legacy experiment consolidation takes too long | Low | Phase 2 deferred; Phase 1 critical path complete | ✅ Accepted |
| Gilbreth queue congestion delays experiments | Medium | Use standby QoS as backup; submit micro-chunks | ✅ Plan in place |

## Next 3 Actions

1. **Monitor 64×64 resolution scaling jobs** — Track job progress on Gilbreth; document results in new experiment note (expt-20251025-e2-res64)
2. **Continue Phase 2 documentation** — Batch-migrate legacy 23 E1 experiments; create remaining job submission notes
3. **Prepare E4 design** — Start N-step returns investigation; draft smoke test plan for 500 episodes

## Links to detailed plans/sources
- Experiments Plan (detailed phases E1–E4): [[01 Projects/ARL-RL/Experiments/Plan]]
- Execution & best practices: [[Submitting SLURM Jobs on Gilbreth for LLMs]], [[Engineering Notes - Mixed Precision and HPC]], [[Common Commands]]
- Decisions guiding the plan: [[01 Projects/ARL-RL/Decisions/Index]]
- Experiments hub and results: [[Experiments]]
- Work in progress/completed: [[01 Projects/ARL-RL/Work Completed/Index]]
- Open tasks: [[01 Projects/AGILE3D-Demo/To Do]], [[01 Projects/ARL-RL/Backlog]]

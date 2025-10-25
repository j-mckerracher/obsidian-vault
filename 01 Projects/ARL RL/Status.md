---
project: ARL RL
tags: [project/arl-rl, status]
created: 2025-10-05
---

# Status — ARL RL

## Overall status (2025-10-21)
|- **Queue stall resolved**: Canceled long-pending standby chain (9774460–9774462, 2+ days queued) and resubmitted as independent normal QoS jobs.
|- **New jobs submitted (normal QoS)**: Seeds 4/6/8, 1k episodes each, 4h wall time, job IDs 9795192/9795193/9795194.
|- **Expected faster turnaround**: Normal QoS priority (vs. standby backfill); independent runs remove dependency chain overhead.
|- **Stage E1 smoke runs completed**: Conducted validation runs at 32×32 with 300 episodes per seed (seeds 4, 6, 8).
|- **Smoke results**: High variance observed (seed 4 = 80%, seed 6 = 0%, seed 8 = 20%; mean 33.3%).
|- SLURM Integration: Complete job submission pipeline with wrapper scripts, documentation, and troubleshooting guides.
|- Stage E1 (Double DQN + LR scheduler) implemented with production-ready SLURM automation.
|- NO_OP behavior fix: Action selection prioritization reduces idling during training.

## Stage E1 Validation & Production Runs (2025-10-21)
**Smoke validation (300 episodes, 32×32, standby QoS - completed):**
- Seed 4 (job 9765383): win_rate=80.0%, avg_reward=2.0
- Seed 6 (job 9766884): win_rate=0.0%, avg_reward=0.0
- Seed 8 (job 9767893): win_rate=20.0%, avg_reward=0.0
- Mean: 33.3% (high variance indicates parameter sensitivity or seed initialization effects)

**Production 1k-episode runs (normal QoS, independent jobs - in progress):**
- Job IDs: 9795192 (seed 4), 9795193 (seed 6), 9795194 (seed 8)
- Configuration: 1,000 episodes per seed, 32×32 resolution, Stage E1 recipe (Double DQN + LR scheduler)
- Wall time: 4 hours per job (normal QoS, expected start within hours)
- Execution: Independent (no dependencies); parallel execution possible if GPUs available
- Note: Canceled prior standby chain (9774460–9774462, 2+ day queue wait) and resubmitted for faster turnaround
- Artifacts will aggregate in: `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/e1_results.csv`

**Completed 2h standby chunks (2025-10-21):** seed4=20%, seed6=40%, seed8=20% (5‑episode tests, ~800 eps each)

**Final 100-episode tests after top-ups (2025-10-21):**
- seed4=59.0%, seed6=0.0%, seed8=73.0%
- Mean=44.0%, StdDev=38.7 pp
- Decision: Proceed to Stage E2 (criteria met: mean ≥ 40% and StdDev < 40 pp)

## Recent results (short sweeps)
- Learning rate (Sweep A, 32×32):
  - 0.00005 → 57.0% win rate (best)
  - 0.00025 → 11.0%
  - 0.00010 → 6.0%
- Epsilon decay (Sweep B, reported LR=0.0001 in CSV; choosing decay for next phase):
  - 20000 → 13.0% (best of sweep)
  - 100000 → 10.0%
  - 50000 → 1.0%
- Target update frequency (Sweep C, CSV shows LR=0.0001, EPS_DECAY=50000; choosing value for next phase):
  - 200 → 53.0% (best)
  - 100 → 9.0%
  - 50 → 2.0%

Notes:
- LR and decay/TUF sweeps were not all run under the final chosen LR/decay combos; confirm runs have now validated the combined choice at 32×32.
- Confirm runs (32×32): seeds 4 → 37.0%, 6 → 29.0%, 8 → 7.0% (mean ≈ 24.3%).

## Current best parameter set (validated at 32×32; mean ≈ 33%)
- LR: 0.00005 (from Sweep A)
- EPS_DECAY: 20000 (from Sweep B)
- TARGET_UPDATE_FREQ: 200 (from Sweep C)
- Other: batch 8, replay 50k, resolution 32×32, step_mul 8

## SLURM Job Submission (2025-10-11)
**Infrastructure**: Complete SLURM integration with multiple submission methods  
**Scripts**: 
- `scripts/run_e1.sh` - Main SLURM job script with SBATCH directives
- `scripts/submit_e1_job.sh` - User-friendly submission wrapper
- `scripts/README_SLURM.md` - Comprehensive documentation

**Environment**: Fixed conda path `/depot/sbagchi/data/preeti/anaconda3/envs/gpu`  
**Validation**: Pre-flight checks, GPU monitoring, error handling  
**Monitoring**: Comprehensive logging and result aggregation  

**Stage E1 Training Configuration**:
- **Default**: 10,000 episodes per seed, seeds 4/6/8, 32x32 resolution
- **Resources**: 1 node, 1 GPU, 12-hour time limit, normal QoS (subject to account policy)
- **Algorithm**: Double DQN + Cosine LR scheduling
- **Parameters**: LR=5e-5, batch_size=4, replay=100k, target_update_freq=300
- **Memory optimized**: Mixed precision + CUDA memory management

## Next actions
- Proceed to E2 (Dueling DQN): implement dueling head on non-spatial branch, keep hyperparams fixed; minimal code diff, then run 300–500‑ep smoke per seed on standby.
- Parallel quick check: submit a short 300‑ep rerun for seed 6 under E1 to sanity‑check the 0% outlier (non‑blocking).
- After E2 smoke: if mean ≥ E1 mean, schedule 1k‑ep confirms per seed via standby chunks; otherwise, consider minor E1 tweak (e.g., TUF 300→200 or 400).

## Risks and watchouts
- GPU contention on shared A30 node can affect training speed/stability.
- Resolution increases will raise memory and compute costs.

## Links
|- **Latest work**: 
  - [[Work Completed/2025-10-21 Queue stall fix - normal QoS resubmission]]
  - [[Work Completed/2025-10-19 Stage E1 smoke runs seeds 6 and 8]]
  - [[Work Completed/2025-10-19 Stage E1 smoke run 300eps seed4]]
  - [[Work Completed/2025-10-19 Stage E1 chained 1k eps seeds 4 6 8]] (canceled/replaced)
|- **Previous fixes**: [[Work Completed/2025-10-11 FP16 masking overflow fix]]
|- **SLURM Integration**: [[Work Completed/2025-10-09 SLURM job submission scripts]]
|- Decisions: [[Decisions/Index]]
|- Experiments hub: [[Experiments]]
|- Issues log: [[Work Completed/2025-10-04 Issues and Solutions]]
|- SLURM docs: [[Documents/Submitting SLURM Jobs on Gilbreth for LLMs]]
|- Common commands: [[Documents/Common Commands]]

---
project: ARL RL
tags: [project/arl-rl, status]
created: 2025-10-05
---

# Status — ARL RL

## Overall Status
**Status**: 🞫 GREEN — Excellent progress on E2 validation; PER exploration completed and parked.

**Last updated**: 2025-11-30T13:05:00Z

### Summary
- **E2 Production Validated**: 3k episodes achieve **94.3% mean win rate** (97%/88%/98%), excellent scaling from 1k (91.3%) and 500 (52.7%)
- **E2 Configuration Frozen**: Dueling DQN with LR=5e-5, TUF=400, locked for production use
- **E3 PER Parked**: Tested α∈{0.4, 0.5, 0.6} with β annealing; no configuration improved over E2 baseline
- **Next Phase**: Resolution scaling (64×64) or E4 (N-step returns) exploration pending user choice
|- SLURM Integration: Complete job submission pipeline with wrapper scripts, documentation, and troubleshooting guides.
|- NO_OP behavior fix: Action selection prioritization reduces idling during training.

## Stage progression summary

**Stage E1 Final (2025-10-21 - completed)**
- 100-episode tests: seed4=59.0%, seed6=0.0%, seed8=73.0%
- Mean=44.0%, StdDev=38.7 pp
- Gate passed: mean ≥ 40% and StdDev < 40 pp
- Decision: Proceed to Stage E2

**Stage E2 Dueling DQN (2025-10-25 - validated at scale)**
- TUF-sweep-alt-3 (500 eps): Mean=52.7%, StdDev=35.9 pp (gate passed)
- run-6 (1k eps): Seeds 4=92.0%, 6=95.0%, 8=87.0% → Mean=91.3%, StdDev=4.0 pp
- **Production (3k eps)**: Seeds 4=97.0%, 6=88.0%, 8=98.0% → **Mean=94.3%, StdDev=5.7 pp**
- **E2 VALIDATED**: Excellent performance at scale with continued improvement
- Configuration frozen and production-ready

**Stage E3 PER Exploration (2025-10-25 - parked)**
- Smoke (α=0.6): Mixed results, seed 8 unstable, below E2 baseline
- Alpha sweep (α=0.4,0.5): All configurations below E2 baseline
- Decision: Park PER; does not improve over E2

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

## Frozen E2 configuration (validated at 32×32; mean = 91.3%)
- DUELING_DQN: enabled
- LR: 5e-5
- EPS_DECAY: 100000
- TARGET_UPDATE_FREQ: 400
- BATCH_SIZE: 4
- REPLAY_MEMORY_SIZE: 100000
- SCREEN_RESOLUTION / MINIMAP_RESOLUTION: 32
- STEP_MUL: 16

## SLURM Job Submission (2025-10-11)
**Infrastructure**: Complete SLURM integration with multiple submission methods  
**Scripts**: 
- `scripts/run_e1.sh` - Main SLURM job script with SBATCH directives
- `scripts/submit_e1_job.sh` - User-friendly submission wrapper
- `scripts/README_SLURM.md` - Comprehensive documentation

**Environment**: Fixed conda path `/depot/<group>/data/<username>/anaconda3/envs/gpu`  
**Validation**: Pre-flight checks, GPU monitoring, error handling  
**Monitoring**: Comprehensive logging and result aggregation  

**Stage E1 Training Configuration**:
- **Default**: 10,000 episodes per seed, seeds 4/6/8, 32x32 resolution
- **Resources**: 1 node, 1 GPU, 12-hour time limit, normal QoS (subject to account policy)
- **Algorithm**: Double DQN + Cosine LR scheduling
- **Parameters**: LR=5e-5, batch_size=4, replay=100k, target_update_freq=300
- **Memory optimized**: Mixed precision + CUDA memory management

## Next actions

> [!IMPORTANT] Decision Point
> Choose next exploration direction. Current recommendation: **Option 1 (Resolution Scaling)** for natural progression without code changes.

### 🔴 Priority 1: Resolution Scaling (64×64) — **RECOMMENDED**
- Test frozen E2 config at higher resolution
- **Why first**: Natural progression from E2 success, no code changes needed, better spatial awareness
- **Resource**: ~4x memory/compute vs 32×32 (80GB mem, 3-4h per seed)
- **Timeline**: 500-1k episode smoke runs per seed
- **Expected**: Potentially >95% win rate with improved tactical decisions
- **Command**: See [[Don't Forget]] for current preferred submission method

### 🟡 Priority 2: Stage E4 (N-step Returns, n=3)
- Add multi-step bootstrapping to E2 baseline
- **Why second**: Requires code implementation first (RL_N_STEP parameter + buffer changes)
- **Resource**: Similar to E2 baseline (50GB mem, 2-3h per seed)
- **Timeline**: Implementation (1-2 days) + 500-1k episode smoke runs per seed
- **Expected**: Improved credit assignment, potentially faster learning

### 🟢 Priority 3: Extended Validation (4k-5k episodes)
- Push E2 even further to test convergence limits
- **Why third**: Only valuable if 64×64 and E4 don't show improvement
- **Resource**: 6-8h per seed on normal QoS
- **Expected**: Marginal improvements or plateau confirmation
- **Timeline**: 1-2 days for full 3-seed run

### 🔵 Priority 4: Checkpoint Cleanup & Deployment Prep
- Archive strategic checkpoints, delete intermediates
- Prepare best model (seed 8 ep3000, 98% win rate) for deployment/demos
- Document final E2 configuration for paper/reports
- **Why last**: Can be done in parallel with any other option


## Risks and watchouts
- GPU contention on shared A30 node can affect training speed/stability.
- Resolution increases will raise memory and compute costs.

## Links
|- **Latest work**: 
  - [[Work Completed/2025-10/2025-10-21#Queue Stall Fix — Normal QoS Resubmission]]
  - [[Work Completed/2025-10/2025-10-19#Stage E1 smoke runs — seeds 6 and 8]]
  - [[Work Completed/2025-10/2025-10-19#Stage E1 smoke run — 1h standby, 32×32, seed 4]]
  - [[Work Completed/2025-10/2025-10-19#Stage E1 chained submissions — standby, 1k eps/seed, 32×32]]
|- **Previous fixes**: [[Work Completed/2025-10/2025-10-11#FP16 masking overflow fix (autocast-safe)]]
|- **SLURM Integration**: [[Work Completed/2025-10/2025-10-09]]
|- Decisions: [[01 Projects/ARL-RL/Decisions/Index]]
|- Experiments hub: [[Experiments]]
|- Issues log: [[Work Completed/2025-10/2025-10-04]]
|- SLURM docs: [[Submitting SLURM Jobs on Gilbreth for LLMs]]
|- Common commands: [[Common Commands]]
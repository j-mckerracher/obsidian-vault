---
project: ARL RL
tags: [project/arl-rl, status]
created: 2025-10-05
---

# Status — ARL RL

## Overall status (2025-10-25)
|- **Stage E2 CONFIRMED**: Dueling DQN with frozen configuration achieves 91.3% mean win rate (seeds 4/6/8: 92%/95%/87%) with 4.0 pp stdev.
|- **Stage E3 PER parked**: Prioritized Experience Replay tested with α∈{0.4,0.5,0.6} and β annealing; all configurations underperformed E2 baseline. Decision: park PER, proceed with E2 production.
|- **Frozen E2 configuration**: LR=5e-5, EPS_DECAY=100k, Batch=4, Replay=100k, Res=32, StepMul=16, TUF=400, Dueling DQN enabled.
|- **Next step**: E2 production runs (2k-4k episodes per seed) to validate long-term stability and performance.
|- SLURM Integration: Complete job submission pipeline with wrapper scripts, documentation, and troubleshooting guides.
|- NO_OP behavior fix: Action selection prioritization reduces idling during training.

## Stage progression summary

**Stage E1 Final (2025-10-21 - completed)**
- 100-episode tests: seed4=59.0%, seed6=0.0%, seed8=73.0%
- Mean=44.0%, StdDev=38.7 pp
- Gate passed: mean ≥ 40% and StdDev < 40 pp
- Decision: Proceed to Stage E2

**Stage E2 Dueling DQN (2025-10-25 - confirmed)**
- TUF-sweep-alt-3 (500 eps): Mean=52.7%, StdDev=35.9 pp (gate passed)
- run-6 (1k eps): Seeds 4=92.0%, 6=95.0%, 8=87.0% → Mean=91.3%, StdDev=4.0 pp
- **E2 CONFIRMED**: Outstanding performance and stability
- Configuration frozen for production

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
- **E2 production runs**: Submit 2k-4k episode runs per seed (seeds 4, 6, 8) with frozen E2 config to validate long-term stability
- **Resource allocation**: Use normal QoS on sbagchi account for production runs
- **Optional exploration**: Consider resolution scaling (64×64) after E2 production validation
- **E4 preparation**: Begin design for N-step returns (n=3) if E2 production results are stable
- **Documentation**: Keep experiments log and frozen config decision up-to-date

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

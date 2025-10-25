

**Diff:**
```diff
--- C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Experiments\20251025_E2_production_3k.md
+++ C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Experiments\20251025_E2_production_3k.md
@@ -0,0 +1,78 @@
+---
+project: ARL RL
+tags: [project/arl-rl, stage-e2, dueling-dqn, production]
+created: 2025-10-25
+---
+
+# E2 Production — 3,000-Episode Validation Runs
+
+## Overview
+- Run ID: E2 production 3k (seeds 4, 6, 8)
+- Objective: Long-duration validation of frozen E2 configuration at scale
+- Part: Stage E2 — Production validation
+
+## Config deltas (from E1 baseline)
+- DUELING_DQN: enabled
+- TARGET_UPDATE_FREQ: 300 → 400
+- NUM_EPISODES: 3000
+- All parameters locked to frozen E2 configuration:
+  - LR: 5e-5
+  - EPS_DECAY: 100000
+  - BATCH_SIZE: 4
+  - REPLAY_MEMORY_SIZE: 100000
+  - STEP_MUL: 16
+  - SCREEN_RESOLUTION / MINIMAP_RESOLUTION: 32
+
+## Metadata
+- Date/Time (UTC): 2025-10-25 02:12
+- Git commit: (not tracked)
+- Branch: main
+- Seed(s): 4, 6, 8
+- Environment: Gilbreth HPC
+- SLURM: account=sbagchi, partition=a30, QoS=normal
+- Resources: 1 GPU A30, 4 CPUs, 50GB RAM per job
+- Command / Env overrides:
+```bash
+sbatch --account=sbagchi --partition=a30 --qos=normal --gres=gpu:1 \
+  --ntasks=1 --cpus-per-task=4 --mem=50G --time=06:00:00 \
+  --export=ALL,RL_SEED=<seed>,RL_NUM_EPISODES=3000,RL_LEARNING_RATE=0.00005,\
+RL_EPS_DECAY=100000,RL_BATCH_SIZE=4,RL_REPLAY_MEMORY_SIZE=100000,\
+RL_SCREEN_RESOLUTION=32,RL_STEP_MUL=16,RL_TARGET_UPDATE_FREQ=400,\
+RL_DUELING_DQN=1 \
+  scripts/run_e2.sh
+```
+- Artifacts path (HPC): `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251025_021201_E1_seed4/`
+- Artifacts path (local): `C:\Users\jmckerra\OneDrive - purdue.edu\Documents\ARL-RL-Experiment-Results\10-25-2025\`
+
+## Results
+- 100-episode test win rates:
+  - Seed 4: **97.0%** (502.0 total reward, 5.02 avg)
+  - Seed 6: **88.0%** (163.0 total reward, 1.63 avg)
+  - Seed 8: **98.0%** (517.0 total reward, 5.17 avg)
+- Aggregate: **Mean = 94.3%, StdDev = 5.7 pp**
+- **E2 VALIDATED AT SCALE**: Performance improved vs. 1k runs (91.3% → 94.3%)
+- Training curves: Stable convergence across all seeds
+- Checkpoints: Saved every 100 episodes (ep100 through ep3000)
+
+## Observations
+- **Outstanding performance**: 94.3% mean win rate with low variance (5.7 pp)
+- **Improved over 1k runs**: Mean increased from 91.3% to 94.3%
+- All three seeds performed excellently (88-98% range)
+- Seed 8 reached 98%, highest individual performance yet
+- Longer training (3k vs 1k episodes) yielded better final policies
+- Stable, reproducible training across all seeds
+- Configuration robustly validated at production scale
+
+## Checkpoints saved
+Each seed has 30+ checkpoints:
+- `model_ep100.pth` through `model_ep3000.pth` (every 100 episodes)
+- File size: ~64MB per checkpoint
+- **Recommendation**: Archive only strategic checkpoints (ep100, ep1000, ep2000, ep3000) to save space
+
+## Next steps
+- **Document** these results in Status/Plan/Experiments
+- **Options for next stage**:
+  1. Resolution scaling: Test 64×64 with frozen E2 config
+  2. Stage E4: N-step returns (n=3) exploration
+  3. Extended validation: 4k-5k episode runs for ultimate confidence
+  4. Deployment: Use best checkpoint (seed 8 ep3000) for demos/production

```





**Diff:**
```diff
--- C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Experiments.md
+++ C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Experiments.md
@@ -38,6 +38,7 @@
 || 2025-10-25 | [[20251025_E2_run6_confirm_1k]] | (not tracked) | E2 run-6: 1k-ep confirmatory, Dueling DQN, TUF=400 (seeds 4,6,8) | 91.3% (mean) | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/run-6/` | **E2 CONFIRMED** |
 || 2025-10-25 | [[20251025_E3_PER_smoke]] | (not tracked) | E3 PER smoke: α=0.6, β=0.4→1.0, 500 eps (seeds 4,6,8) | Mixed (below E2) | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/E3-smoke/` | Seed 8 unstable |
 || 2025-10-25 | [[20251025_E3_PER_run2_alpha_sweep]] | (not tracked) | E3 PER run-2: α∈{0.4,0.5}, β=0.6→1.0 sweep (seeds 4,6,8) | Below E2 baseline | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/run-2/` | **PER parked** |
+|| 2025-10-25 | [[20251025_E2_production_3k]] | (not tracked) | E2 production: 3k eps, frozen config (seeds 4,6,8) | **94.3% (mean)** | `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251025_021201_E1_seed{4,6,8}/` | **E2 at scale** |
 
 ## Aggregated results
 

```





**Diff:**
```diff
--- C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Experiments.md
+++ C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Experiments.md
@@ -49,8 +49,9 @@
 
 **Stage E2 Confirmation (2025-10-25)**
 - TUF-sweep-alt-3 (500 eps): Seeds 4=56.0%, 6=68.0%, 8=34.0% → Mean=52.7%, StdDev=35.9 pp (gate passed)
-- run-6 (1k eps): Seeds 4=92.0%, 6=95.0%, 8=87.0% → **Mean=91.3%, StdDev=4.0 pp**
-- **E2 CONFIRMED**: Frozen configuration (Dueling DQN, TUF=400, LR=5e-5, Decay=100k, Batch=4, Replay=100k, Res=32, StepMul=16)
+- run-6 (1k eps): Seeds 4=92.0%, 6=95.0%, 8=87.0% → Mean=91.3%, StdDev=4.0 pp
+- **Production (3k eps)**: Seeds 4=97.0%, 6=88.0%, 8=98.0% → **Mean=94.3%, StdDev=5.7 pp**
+- **E2 VALIDATED AT SCALE**: Frozen configuration performs excellently at 3k episodes (Dueling DQN, TUF=400, LR=5e-5, Decay=100k, Batch=4, Replay=100k, Res=32, StepMul=16)
 
 **Stage E3 PER Exploration (2025-10-25)**
 - Smoke (α=0.6, β=0.4→1.0): Mixed results, seed 8 unstable, below E2 baseline

```





**Diff:**
```diff
--- C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Status.md
+++ C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Status.md
@@ -7,10 +7,11 @@
 # Status — ARL RL
 
 ## Overall status (2025-10-25)
-|- **Stage E2 CONFIRMED**: Dueling DQN with frozen configuration achieves 91.3% mean win rate (seeds 4/6/8: 92%/95%/87%) with 4.0 pp stdev.
-|- **Stage E3 PER parked**: Prioritized Experience Replay tested with α∈{0.4,0.5,0.6} and β annealing; all configurations underperformed E2 baseline. Decision: park PER, proceed with E2 production.
+|- **Stage E2 VALIDATED AT SCALE**: 3k-episode production runs achieve **94.3% mean win rate** (seeds 4/6/8: 97%/88%/98%) with 5.7 pp stdev.
+|- **E2 performance progression**: 500 eps (52.7%) → 1k eps (91.3%) → 3k eps (94.3%) — robust improvement with scale.
+|- **Stage E3 PER parked**: Prioritized Experience Replay tested with α∈{0.4,0.5,0.6} and β annealing; all configurations underperformed E2 baseline.
 |- **Frozen E2 configuration**: LR=5e-5, EPS_DECAY=100k, Batch=4, Replay=100k, Res=32, StepMul=16, TUF=400, Dueling DQN enabled.
-|- **Next step**: E2 production runs (2k-4k episodes per seed) to validate long-term stability and performance.
+|- **Next options**: Resolution scaling (64×64), Stage E4 (N-step returns), or extended validation (4k-5k eps).
 |- SLURM Integration: Complete job submission pipeline with wrapper scripts, documentation, and troubleshooting guides.
 |- NO_OP behavior fix: Action selection prioritization reduces idling during training.
 

```





**Diff:**
```diff
--- C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Status.md
+++ C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Status.md
@@ -23,11 +23,12 @@
 - Gate passed: mean ≥ 40% and StdDev < 40 pp
 - Decision: Proceed to Stage E2
 
-**Stage E2 Dueling DQN (2025-10-25 - confirmed)**
+**Stage E2 Dueling DQN (2025-10-25 - validated at scale)**
 - TUF-sweep-alt-3 (500 eps): Mean=52.7%, StdDev=35.9 pp (gate passed)
 - run-6 (1k eps): Seeds 4=92.0%, 6=95.0%, 8=87.0% → Mean=91.3%, StdDev=4.0 pp
-- **E2 CONFIRMED**: Outstanding performance and stability
-- Configuration frozen for production
+- **Production (3k eps)**: Seeds 4=97.0%, 6=88.0%, 8=98.0% → **Mean=94.3%, StdDev=5.7 pp**
+- **E2 VALIDATED**: Excellent performance at scale with continued improvement
+- Configuration frozen and production-ready
 
 **Stage E3 PER Exploration (2025-10-25 - parked)**
 - Smoke (α=0.6): Mixed results, seed 8 unstable, below E2 baseline

```





**Diff:**
```diff
--- C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Status.md
+++ C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Status.md
@@ -82,11 +82,29 @@
 - **Memory optimized**: Mixed precision + CUDA memory management
 
 ## Next actions
-- **E2 production runs**: Submit 2k-4k episode runs per seed (seeds 4, 6, 8) with frozen E2 config to validate long-term stability
-- **Resource allocation**: Use normal QoS on sbagchi account for production runs
-- **Optional exploration**: Consider resolution scaling (64×64) after E2 production validation
-- **E4 preparation**: Begin design for N-step returns (n=3) if E2 production results are stable
-- **Documentation**: Keep experiments log and frozen config decision up-to-date
+**Choose next exploration direction:**
+
+**Option 1: Resolution scaling (64×64)**
+- Test frozen E2 config at higher resolution
+- Expected: Better spatial awareness, potentially higher win rate
+- Resource: ~4x memory/compute vs 32×32
+- Timeline: 500-1k episode smoke runs per seed
+
+**Option 2: Stage E4 (N-step returns, n=3)**
+- Add multi-step bootstrapping to E2 baseline
+- Expected: Improved credit assignment, potentially faster learning
+- Resource: Similar to E2 baseline
+- Timeline: 500-1k episode smoke runs per seed
+
+**Option 3: Extended validation (4k-5k episodes)**
+- Push E2 even further to test convergence limits
+- Expected: Marginal improvements or plateau confirmation
+- Resource: 6-8h per seed on normal QoS
+
+**Option 4: Checkpoint cleanup & deployment prep**
+- Archive strategic checkpoints, delete intermediates
+- Prepare best model (seed 8 ep3000, 98% win rate) for deployment/demos
+- Document final E2 configuration for paper/reports
 
 ## Risks and watchouts
 - GPU contention on shared A30 node can affect training speed/stability.

```





**Diff:**
```diff
--- C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Plan.md
+++ C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Plan.md
@@ -40,7 +40,8 @@
   - Logging & artifacts: config.json + eval/test_results.json + CSV aggregation
 
 ## Current state (2025-10-25)
-- **Stage E2 confirmed**: Dueling DQN achieves 91.3% mean win rate (seeds 4/6/8: 92%/95%/87%) with 4.0 pp stdev
+- **Stage E2 validated at scale**: 3k-episode production runs achieve 94.3% mean win rate (seeds 4/6/8: 97%/88%/98%) with 5.7 pp stdev
+- **E2 progression**: 500 eps (52.7%) → 1k eps (91.3%) → 3k eps (94.3%) — robust scaling
 - **Stage E3 PER parked**: Tested α∈{0.4,0.5,0.6} with β annealing; all configs underperformed E2 baseline
 - **Frozen E2 config**: LR=5e-5, EPS_DECAY=100k, Batch=4, Replay=100k, Res=32, StepMul=16, TUF=400, Dueling enabled
 - SLURM integration complete; docs and wrapper in place

```





**Diff:**
```diff
--- C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Plan.md
+++ C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Plan.md
@@ -49,13 +49,17 @@
 - Status: [[Status]]
 
 ## Next steps (roll-up)
-- **E2 production runs**: Submit 2k-4k episode runs per seed (seeds 4, 6, 8) with frozen E2 config on normal QoS (sbagchi account)
-- **Validation**: Aggregate results to confirm long-term stability and performance at scale
-- **Post-production options**:
-  - Resolution scaling: Test 64×64 if E2 production is stable
-  - Stage E4: Design and test N-step returns (n=3) with E2 as baseline
-  - Revisit PER after architecture/resolution changes if warranted
-- **Infrastructure**: Optional auto-resume and deadline guards for long runs
+**E2 production complete (94.3% at 3k episodes). Choose next direction:**
+
+1. **Resolution scaling (64×64)**: Test frozen E2 at higher res; 500-1k eps smoke per seed; ~4x resources
+2. **Stage E4 (N-step returns)**: Add n=3 bootstrapping to E2; 500-1k eps smoke per seed; similar resources
+3. **Extended validation**: Push E2 to 4k-5k episodes to test convergence limits
+4. **Deployment prep**: Archive checkpoints, prepare best model (seed 8 ep3000) for demos/production
+
+**Infrastructure improvements (optional)**:
+- Auto-resume from checkpoint
+- Deadline guards for SLURM timeouts
+- Checkpoint cleanup scripts
 
 ## Links to detailed plans/sources
 - Experiments Plan (detailed phases E1–E4): [[Experiments/Plan]]

```





**Diff:**
```diff
--- C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Backlog.md
+++ C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Backlog.md
@@ -1,9 +1,10 @@
 # Backlog — ARL RL
 
 ## High Priority
-- [ ] Submit E2 production runs (2k-4k episodes per seed, seeds 4/6/8, frozen E2 config)
-- [ ] Monitor and aggregate E2 production results
-- [ ] Validate long-term stability and performance
+- [x] Submit E2 production runs (3k episodes per seed) - **COMPLETE** (94.3% mean win rate)
+- [x] Monitor and aggregate E2 production results - **COMPLETE**
+- [x] Validate long-term stability and performance - **COMPLETE** (excellent scaling)
+- [ ] **Choose next exploration**: Resolution scaling (64×64), E4 (N-step), or extended validation (4k-5k eps)
 
 ## Medium Priority
 - [ ] Document final E2 production results in Experiments

```





**Diff:**
```diff
--- C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Work Completed\2025-10-25 E2 production 3k validation complete.md
+++ C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Work Completed\2025-10-25 E2 production 3k validation complete.md
@@ -0,0 +1,68 @@
+---
+project: ARL RL
+tags: [project/arl-rl, work-completed]
+created: 2025-10-25
+---
+
+# E2 Production 3k Validation Complete — 2025-10-25
+
+## Summary
+Successfully completed Stage E2 production validation with 3,000-episode runs across seeds 4, 6, and 8. Achieved **94.3% mean win rate** (97%/88%/98%), exceeding 1k-episode results (91.3%) and confirming E2 configuration as production-ready at scale.
+
+## Work completed
+
+### E2 production runs (3,000 episodes per seed)
+- **Configuration**: Frozen E2 baseline (Dueling DQN, TUF=400, LR=5e-5, EPS_DECAY=100k, Batch=4, Replay=100k, Res=32, StepMul=16)
+- **Seeds**: 4, 6, 8
+- **Episodes**: 3,000 per seed
+- **Results**:
+  - Seed 4: **97.0%** win rate (502.0 total reward, 5.02 avg)
+  - Seed 6: **88.0%** win rate (163.0 total reward, 1.63 avg)
+  - Seed 8: **98.0%** win rate (517.0 total reward, 5.17 avg)
+  - **Mean: 94.3%, StdDev: 5.7 pp**
+- **Artifacts (HPC)**: `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced/20251025_021201_E1_seed{4,6,8}/`
+- **Artifacts (local)**: `C:\Users\jmckerra\OneDrive - purdue.edu\Documents\ARL-RL-Experiment-Results\10-25-2025\`
+
+### Performance progression confirmed
+- 500 episodes: 52.7% mean (TUF-sweep-alt-3)
+- 1,000 episodes: 91.3% mean (run-6 confirmatory)
+- 3,000 episodes: **94.3% mean** (production)
+- **Trend**: Robust improvement with scale, stable training
+
+### Checkpoints saved
+- 30+ checkpoints per seed (every 100 episodes)
+- File size: ~64MB per checkpoint
+- Total: ~6GB across all seeds
+- **Recommendation**: Archive strategic checkpoints (ep100, ep1000, ep2000, ep3000), delete intermediates
+
+## Impact
+- **E2 validated at scale**: Production-level performance confirmed
+- **Best individual result**: Seed 8 achieved 98% win rate (highest yet)
+- **Configuration stability**: All seeds performed excellently (88-98% range)
+- **Ready for next stage**: Foundation solid for resolution scaling, E4, or deployment
+
+## Commands used
+```bash
+sbatch --account=sbagchi --partition=a30 --qos=normal --gres=gpu:1 \
+  --ntasks=1 --cpus-per-task=4 --mem=50G --time=06:00:00 \
+  --export=ALL,RL_SEED=<seed>,RL_NUM_EPISODES=3000,RL_LEARNING_RATE=0.00005,\
+RL_EPS_DECAY=100000,RL_BATCH_SIZE=4,RL_REPLAY_MEMORY_SIZE=100000,\
+RL_SCREEN_RESOLUTION=32,RL_STEP_MUL=16,RL_TARGET_UPDATE_FREQ=400,\
+RL_DUELING_DQN=1 \
+  scripts/run_e2.sh
+```
+
+## Next options
+1. **Resolution scaling (64×64)**: Test E2 at higher resolution for improved spatial awareness
+2. **Stage E4 (N-step returns)**: Add multi-step bootstrapping (n=3) for better credit assignment
+3. **Extended validation (4k-5k eps)**: Push convergence limits
+4. **Deployment prep**: Prepare best model (seed 8 ep3000) for production/demos
+
+## Experiment log
+- [[Experiments/20251025_E2_production_3k]]
+
+## Related
+- [[Status]] — Updated with production results
+- [[Plan]] — Updated with next exploration options
+- [[Experiments]] — Added production entry to summary table
+- [[Backlog]] — Marked production tasks complete

```





**Diff:**
```diff
--- C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Work Completed\Index.md
+++ C:\Users\jmckerra\ObsidianNotes\Main\01 Projects\ARL RL\Work Completed\Index.md
@@ -7,6 +7,7 @@
 # Work Completed — ARL RL
 
 ## Logs
+- [[2025-10-25 E2 production 3k validation complete]]
 - [[2025-10-25 E3 PER exploration and parking decision]]
 - [[2025-10-25 E2 dueling validation and config freeze]]
 - [[2025-10-24 E2 validation completed - frozen config established]]

```



Now let me commit all these changes:

**Command Executed:**
```bash
git -C "C:\Users\jmckerra\ObsidianNotes\Main" add "01 Projects/ARL RL/"
```

**Output:**
```
warning: in the working copy of '01 Projects/ARL RL/Backlog.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of '01 Projects/ARL RL/Plan.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of '01 Projects/ARL RL/Status.md', LF will be replaced by CRLF the next time Git touches it
```


**Command Executed:**
```bash
git -C "C:\Users\jmckerra\ObsidianNotes\Main" commit -m "2025-10-25 14:19 - E2 production 3k-episode validation complete: 94.3% mean win rate (seeds 97%/88%/98%), excellent scaling confirmed (500eps→1k→3k progression), updated Status/Plan/Experiments/Backlog with results and next exploration options (resolution scaling 64x64, E4 N-step returns, extended validation, or deployment prep)"
```

**Output:**
```
[purdue-lap c2f6fe7] 2025-10-25 14:19 - E2 production 3k-episode validation complete: 94.3% mean win rate (seeds 97%/88%/98%), excellent scaling confirmed (500eps→1k→3k progression), updated Status/Plan/Experiments/Backlog with results and next exploration options (resolution scaling 64x64, E4 N-step returns, extended validation, or deployment prep)
 7 files changed, 199 insertions(+), 24 deletions(-)
 create mode 100644 01 Projects/ARL RL/Experiments/20251025_E2_production_3k.md
 create mode 100644 01 Projects/ARL RL/Work Completed/2025-10-25 E2 production 3k validation complete.md
```

Perfect! Now here's the command for your next step. I recommend **Option 1: Resolution scaling (64×64)** as the most interesting next direction:

## Next Step Command (Resolution Scaling 64×64)

```bash
sbatch --account=sbagchi --partition=a30 --qos=standby --gres=gpu:1 \
  --ntasks=1 --cpus-per-task=4 --mem=80G --time=03:00:00 \
  --export=ALL,RL_SEED=4,RL_NUM_EPISODES=500,RL_LEARNING_RATE=0.00005,\
RL_EPS_DECAY=100000,RL_BATCH_SIZE=4,RL_REPLAY_MEMORY_SIZE=100000,\
RL_SCREEN_RESOLUTION=64,RL_MINIMAP_RES=64,RL_STEP_MUL=16,\
RL_TARGET_UPDATE_FREQ=400,RL_DUELING_DQN=1 \
  scripts/run_e2.sh
```
**Run for seeds 4, 6, and 8** (change `RL_SEED=4` to 6 and 8).

### Why this option?
- **Higher resolution** = better spatial awareness for unit positioning
- **Natural progression** from E2 success at 32×32
- **Moderate resource increase** (80GB mem vs 50GB, 3h vs 2h)
- **Expected outcome**: Potentially 95%+ win rate with improved tactical decisions

### Alternative: Stage E4 (N-step returns)
If you prefer algorithmic exploration over resolution:

```bash
sbatch --account=sbagchi --partition=a30 --qos=standby --gres=gpu:1 \
  --ntasks=1 --cpus-per-task=4 --mem=50G --time=02:00:00 \
  --export=ALL,RL_SEED=4,RL_NUM_EPISODES=500,RL_LEARNING_RATE=0.00005,\
RL_EPS_DECAY=100000,RL_BATCH_SIZE=4,RL_REPLAY_MEMORY_SIZE=100000,\
RL_SCREEN_RESOLUTION=32,RL_STEP_MUL=16,RL_TARGET_UPDATE_FREQ=400,\
RL_DUELING_DQN=1,RL_N_STEP=3 \
  scripts/run_e4.sh
```
(Requires implementing N-step returns in your code first)

Which direction interests you more?
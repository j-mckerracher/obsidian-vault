# Backlog — ARL RL

## High Priority
- [x] Submit E2 production runs (3k episodes per seed) - **COMPLETE** (94.3% mean win rate)
- [x] Monitor and aggregate E2 production results - **COMPLETE**
- [x] Validate long-term stability and performance - **COMPLETE** (excellent scaling)
- [ ] **Choose next exploration**: Resolution scaling (64×64), E4 (N-step), or extended validation (4k-5k eps)

## Medium Priority
- [ ] Document final E2 production results in Experiments
- [ ] Design E4 (N-step returns, n=3) experiment plan
- [ ] Consider resolution scaling test (64×64) after E2 production

## Low Priority / Future
- [ ] Revisit PER after architecture/resolution changes
- [ ] Add auto-resume from checkpoint feature
- [ ] Add deadline guard to save before SLURM timeout
- [ ] Explore multi-seed aggregation for policy ensembles


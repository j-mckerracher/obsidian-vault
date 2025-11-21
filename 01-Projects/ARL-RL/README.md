# ARL-RL Project — Quick Start for AI Agents

> [!NOTE] Last Updated
> 2025-11-20 by Josh McKeracher

## 🎯 Current Status

**Phase**: Stage E2 Production Validated ✅  
**Achievement**: **94.3% mean win rate** at 3,000 episodes (seeds 4/6/8: 97%/88%/98%)  
**Progress**: E1 (44% → E2 @ 52.7% → 91.3% → **94.3%**) — Excellent scaling confirmed

**Current Decision Point**: Choose next exploration direction (see Next Actions below)

---

## 🔴 Immediate Next Action

**PRIORITY**: Submit 64×64 Resolution Scaling Jobs

**Why**: Natural progression from E2 success; test if higher resolution improves spatial awareness  
**Status**: 4 jobs pending in queue (3 with `AssocGrpGRES` blocking, 1 waiting on resources)  
**Blocker**: Old jobs may need cancellation

**Command** (after checking/canceling old jobs):
```bash
cd /home/jmckerra/Code/ARL-RL

sbatch --account sbagchi --partition a30 --qos standby \
  --time 4:00:00 --mem 80G \
  scripts/run_e2.sh --res 64 --seeds "4 6 8" --episodes 500
```

See [[Don't Forget]] for preferred submission patterns.

---

## 📍 Quick Navigation

### Core Documentation
- **[[Status]]** — Current status, recent results, stage progression
- **[[Plan]]** — Overarching roadmap, milestones, risk tracking
- **[[Experiments]]** — Canonical experiment tracker with all runs
- **[[RESULTS_SUMMARY]]** — Executive summary for research reporting

### Finding Information
- **Decisions**: [[Decisions/Index]] — Key choices with rationale
- **Work Logs**: [[Work-Log/Index]] — Chronological work history
- **How-To Guides**: [[Documents/Index]] — SLURM, commands, engineering notes
- **Scripts**: [[Scripts-Reference/README|Scripts Reference]] — Reference copies of SLURM job scripts

---

## 🧠 Recent Context (Last 3 Sessions)

### 2025-11-20: Queue Troubleshooting & Job Submission
- Checked SLURM queue: 4 E2_Training jobs pending
- 3 jobs blocked by `AssocGrpGRES` (account GPU limit)
- 1 job waiting on general resources
- Updated [[Don't Forget]] with standby QoS preference
- **Action needed**: Cancel old jobs 9821750-52, keep 9974636

### 2025-10-25: E2 Production Validation Complete
- Completed 3k-episode runs across seeds 4, 6, 8
- Results: 97%/88%/98% → **94.3% mean** (excellent!)
- Updated Status, Plan, Experiments with results
- Parked E3 (PER) — underperformed E2 baseline
- Created decision point for next direction

### 2025-10-25: E3 PER Exploration
- Tested Prioritized Experience Replay with α∈{0.4, 0.5, 0.6}
- All configurations below E2 baseline
- Decision: Park PER, proceed with E2 as foundation

---

## 🚧 Known Issues & Blockers

### Active Blockers
- **SLURM Queue**: 3 jobs hitting `AssocGrpGRES` limit (need cancellation)
- **Decision Point**: Need to choose next exploration direction

### Configuration Notes
- **Frozen E2 Config**: LR=5e-5, TUF=400, Batch=4, Replay=100k, Res=32, StepMul=16, Dueling=1
- **Preferred QoS**: Use `standby` to avoid group GPU limits (see [[Don't Forget]])
- **Account**: `sbagchi` on Gilbreth cluster

---

## 📊 Key Results Summary

| Stage | Algorithm | Episodes | Win Rate | Status |
|-------|-----------|----------|----------|--------|
| E1 | Double DQN + LR Scheduler | 1k | 44.0% | ✅ Complete |
| E2 (500) | + Dueling DQN | 500 | 52.7% | ✅ Gate passed |
| E2 (1k) | + TUF=400 | 1k | 91.3% | ✅ Confirmed |
| **E2 (3k)** | **Frozen Config** | **3k** | **94.3%** | ✅ **Production** |
| E3 | + PER | 500 | <E2 | ⏸️ Parked |

---

## 🎓 For New AI Agents

**If you're starting fresh**, read in this order:
1. This README (you are here!)
2. [[Status]] — detailed current state
3. [[Plan]] — understand the roadmap
4. [[Experiments]] — see experiment history

**Common tasks**:
- Check queue: `squeue -u $USER`
- Submit job: See [[Don't Forget]] for current preferred method
- Review results: Check [[Experiments]] table
- Update docs: [[Status]], [[Plan]], [[Experiments]] after major work

**Communication**:
- Principal Researcher: Likely wants updates via [[RESULTS_SUMMARY]]
- Daily work: Add to [[Work Completed/Index]]
- Decisions: Document in [[Decisions/]] with context

---

## 🔗 External Resources

- **Code Repository**: `/home/jmckerra/Code/ARL-RL` on Gilbreth
- **Results Path**: `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced`
- **Local Results**: `C:\Users\jmckerra\OneDrive - purdue.edu\Documents\ARL-RL-Experiment-Results\`
- **Cluster**: Gilbreth HPC (Purdue)

---

*This README is maintained as the single source of truth for AI agent onboarding. Update after major milestones or decision points.*

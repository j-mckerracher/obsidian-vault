# Don't Forget — ARL RL

> [!note] Critical reminders
> Add key facts, deadlines, or gotchas here.

## URGENT: Restart Stage E1 Training (After OOM Fix - 2025-10-06)

**Status**: Overnight E1 run hit OOM. Fixed with optimizer preallocation + reduced batch size.

**To restart on Gilbreth**:
```bash
# Pull latest fixes
cd ~/Code/ARL-RL && git pull origin double-dqn

# Restart with fixed configuration
bash scripts/wait_and_run_e1.sh --min-free 2048 --sleep 300 --timeout 7200 --fallback-batch 2 -- --res 32 > e1_master.log 2>&1 &

# Monitor
tail -f e1_master.log
```

**Key changes**:
- Batch size: 8 → 4 (40-50% less memory)
- Optimizer state preallocation (fails fast)
- Enhanced CUDA allocator config
- Training time: ~10-15 hours (up from 8-10)

**Success indicators**:
- "Preallocating optimizer state" message
- Training starts episode 1 without OOM
- GPU memory ~2-3 GB stable

See [[2025-10-06 OOM fix and memory optimizations]] for details.

---

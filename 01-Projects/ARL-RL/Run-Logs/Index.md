---
project: ARL RL
tags: [project/arl-rl, logs, archived]
created: 2025-11-20
---

# Run Logs — ARL RL

This directory contains raw SLURM output logs and training execution logs from the Gilbreth HPC cluster.

## Purpose

Archived logs for:
- Debugging failed training runs
- Verifying experiment execution details
- Auditing resource usage and performance
- Historical record of job submissions

## Contents

### Stage E1 Training Logs (October 2025)
- `20251019_033706_E1_seed4.log` — 69KB
- `20251019_041819_E1_seed6.log` — 69KB
- `20251019_151225_E1_seed8.log` — 69KB
- `20251019_162934_E1_seed4.log` — 242KB
- `20251019_170921_E1_seed6.log` — 242KB
- `20251019_175131_E1_seed8.log` — 242KB
- Additional logs and subdirectories

**Total**: 9 log files + 1 subdirectory

## Organization

Logs are named with format: `YYYYMMDD_HHMMSS_<stage>_seed<N>.log`

## Location on HPC

Live logs on Gilbreth: `/depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/logs/`

## Related

- [[Experiments]] — Canonical experiment tracker
- [[Work Completed/Index]] — Work logs with high-level summaries
- [[Documents/Common Commands]] — Commands for accessing logs

## Notes

> [!NOTE]
> These are raw logs for reference only. For experiment results and analysis, see [[Experiments]] and individual experiment notes.

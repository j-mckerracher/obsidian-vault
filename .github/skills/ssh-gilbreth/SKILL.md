---
name: ssh-gilbreth
description: Connect to the Gilbreth HPC cluster via SSH and run remote commands. Use when asked to check job status, submit jobs, inspect files, or perform any task on the Gilbreth cluster.
---

## Connect

```bash
ssh <username>@gilbreth.rcac.purdue.edu
```

Key-based authentication is already configured — no password prompt expected. If prompted for a password, the SSH key is missing or the agent is not running.

## Useful locations on Gilbreth

| Purpose | Path |
|---|---|
| Pipeline code | `/home/<username>/Code/FRESCO-Pipeline/` |
| Source shards | `/depot/<group>/data/josh/FRESCO/chunks/` |
| v3 output root | `/depot/<group>/data/josh/FRESCO/chunks-v3/` |
| Archive | `/depot/<group>/data/josh/FRESCO-Research/runs/` |
| SLURM logs | `/home/<username>/Code/FRESCO-Pipeline/logs/` |

## Common remote tasks

### Check job status
```bash
squeue -u <username>
squeue -u <username> --start          # estimated start time for pending jobs
squeue -A <group>                   # all group jobs
slist                               # group GPU quota summary
```

### Inspect a specific job
```bash
scontrol show job <JOBID>           # full details including pending reason
sacct -j <JOBID> --format=JobID,JobName,State,Elapsed,ExitCode -X
```

### View job output
```bash
tail -f /home/<username>/Code/FRESCO-Pipeline/logs/production_v3_<JOBID>.out
tail -f /home/<username>/Code/FRESCO-Pipeline/logs/production_v3_<JOBID>.err
```

### Cancel a job
```bash
scancel <JOBID>
```

### Activate the conda environment
```bash
conda activate fresco_v2
```

### Patch a remote script
```bash
sed -i 's/--partition=a10/--partition=a100-80gb/' \
  /home/<username>/Code/FRESCO-Pipeline/production_v3.slurm
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Job pending with `AssocGrpGRES` | Wrong partition or group quota full | See `submit-slurm-job` skill |
| `Permission denied (publickey)` | SSH key not loaded | Run `ssh-add ~/.ssh/id_rsa` locally |
| `conda: command not found` | Module not loaded | Run `module load anaconda` first |
| Depot path not found | Depot mount delayed | Wait and retry; check `df -h` |

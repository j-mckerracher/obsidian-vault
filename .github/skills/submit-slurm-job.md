# Skill: Submit a SLURM Job on Gilbreth

## Required SLURM header (production build)

```bash
#SBATCH --job-name=fresco_v3_production
#SBATCH --output=logs/production_v3_%j.out
#SBATCH --error=logs/production_v3_%j.err
#SBATCH --time=12:00:00
#SBATCH --mem=128G
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --partition=a100-80gb        # ONLY valid partition for <group> account
#SBATCH --mail-type=ALL
#SBATCH --mail-user=<personal-email>
```

> ⚠️ **Never use `--partition=a10`, `a30`, `a100-40gb`, or `h100`** — the `<group>` account has zero allocation on those. The job will queue forever with `AssocGrpGRES`. See `gilbreth-preflight` skill.

## Submission

Use `sbbest` (auto-selects least-busy compatible node) when partition flexibility is acceptable:

```bash
cd /home/<username>/Code/FRESCO-Pipeline
sbbest production_v3.slurm
```

Or submit explicitly to `a100-80gb`:

```bash
sbatch --partition=a100-80gb --account=<group> production_v3.slurm
```

## Monitoring commands

```bash
squeue -u $USER                         # your jobs and their state
squeue -u $USER --start                 # estimated start times
squeue -A <group>                       # all group jobs (see who's using GPU quota)
slist                                   # group GPU allocation summary

sacct -j <JOBID> --format=JobID,JobName,State,Elapsed,Timelimit,Start,End,ExitCode -X
scontrol show job <JOBID>               # full job details including reason for pending

scancel <JOBID>                         # cancel a job
```

## Runbook constraint

After submission, **wait 10 minutes**, then **only proceed if the job is RUNNING or COMPLETED**. If still PENDING, stop and wait for user signal before taking further action.

## Common failure: AssocGrpGRES

If a job shows `Reason=AssocGrpGRES`:
1. Check `scontrol show job <JOBID>` → look at `ReqTRES` to see what GPU type was requested.
2. Check `slist` to see the group's current GPU usage.
3. If the wrong GPU type was requested, cancel the job, fix the `--partition` and `--gres` in the script, and resubmit.
4. If the right GPU type was requested but quota is full, wait for a running group job to finish.

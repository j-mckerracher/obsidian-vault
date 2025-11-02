```bash
jid4=$(sbatch --account <group> --partition a30 --qos normal --time 12:00:00 --ntasks=1 --cpus-per-task=4 --mem=50G --gres=gpu:1 /home/<username>/Code/ARL-RL/scripts/run_e1.sh --res 32 --episodes 4000 --seeds "4" | awk '{print $4}'); jid6=$(sbatch --dependency=afterok:$jid4 --account <group> --partition a30 --qos normal --time 12:00:00 --ntasks=1 --cpus-per-task=4 --mem=50G --gres=gpu:1 /home/<username>/Code/ARL-RL/scripts/run_e1.sh --res 32 --episodes 4000 --seeds "6" | awk '{print $4}'); jid8=$(sbatch --dependency=afterok:$jid6 --account <group> --partition a30 --qos normal --time 12:00:00 --ntasks=1 --cpus-per-task=4 --mem=50G --gres=gpu:1 /home/<username>/Code/ARL-RL/scripts/run_e1.sh --res 32 --episodes 4000 --seeds "8" | awk '{print $4}'); echo "Submitted: 4=$jid4 6=$jid6 8=$jid8"
```

check status:
```bash
for j in $jid4 $jid6 $jid8; do f=$(scontrol show job $j | awk -F= '/StdOut=/{print $2}'); echo "$j $f"; done
```

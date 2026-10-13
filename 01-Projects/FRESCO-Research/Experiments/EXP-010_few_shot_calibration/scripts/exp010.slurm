#!/bin/bash
#SBATCH --job-name=EXP010
#SBATCH --output=/home/<username>/Experiments/EXP-010_few_shot_calibration/logs/exp010_%j.out
#SBATCH --error=/home/<username>/Experiments/EXP-010_few_shot_calibration/logs/exp010_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --partition=a30
#SBATCH --account=<group>
#SBATCH --qos=standby
#SBATCH --mail-user=<redacted>@purdue.edu
#SBATCH --mail-type=END,FAIL

set -euo pipefail

EXP_DIR=/home/<username>/Experiments/EXP-010_few_shot_calibration
FRESCO_DIR=/depot/<group>/data/josh/FRESCO/chunks

mkdir -p "$EXP_DIR/logs" "$EXP_DIR/results"

VENV_DIR="${SLURM_TMPDIR:-/tmp}/exp010_venv_${SLURM_JOB_ID:-manual}"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip --quiet
pip install pandas pyarrow duckdb scikit-learn numpy xgboost --quiet

python "$EXP_DIR/scripts/exp010_few_shot_calibration.py" \
  --input-dir "$FRESCO_DIR" \
  --out-dir "$EXP_DIR/results" \
  --threads 16 \
  --n-boot 200

echo "EXP-010 complete"

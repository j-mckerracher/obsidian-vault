#!/bin/bash
#SBATCH --job-name=EXP005_verify
#SBATCH --output=/home/<username>/Experiments/EXP-005_anvil_verification/logs/exp005_%j.out
#SBATCH --error=/home/<username>/Experiments/EXP-005_anvil_verification/logs/exp005_%j.err
#==============================================================================
#                        RESOURCES
#==============================================================================
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=02:00:00
#==============================================================================
#                PLACEMENT & POLICY
#==============================================================================
#SBATCH --partition=a30
#SBATCH --account=<group>
#SBATCH --qos=standby
#SBATCH --mail-user=<redacted>@purdue.edu
#SBATCH --mail-type=END,FAIL

set -euo pipefail

EXP_DIR=/home/<username>/Experiments/EXP-005_anvil_verification
FRESCO_DIR=/depot/<group>/data/josh/FRESCO/chunks

mkdir -p "$EXP_DIR/logs" "$EXP_DIR/results"

# Create venv
VENV_DIR="${SLURM_TMPDIR:-/tmp}/exp005_venv_${SLURM_JOB_ID:-manual}"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip --quiet
python -m pip install -r "$EXP_DIR/scripts/requirements.txt" --quiet

cd "$EXP_DIR"

python "$EXP_DIR/scripts/exp005_anvil_verification.py" train \
  --input-dir "$FRESCO_DIR" \
  --out-dir "$EXP_DIR/results" \
  --threads 16

echo "EXP-005 complete"

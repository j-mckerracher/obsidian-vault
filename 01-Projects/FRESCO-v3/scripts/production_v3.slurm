#!/bin/bash
#SBATCH --job-name=fresco_v3_production
#SBATCH --output=logs/production_v3_%j.out
#SBATCH --error=logs/production_v3_%j.err
#SBATCH --time=12:00:00
#SBATCH --mem=128G
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --partition=a100-80gb
#SBATCH --mail-type=ALL
#SBATCH --mail-user=<personal-email>

# FRESCO v3 Production Data Build
# Processes raw FRESCO shards -> chunks-v3/ with schema normalization

echo "========================================"
echo "FRESCO v3 PRODUCTION DATA BUILD"
echo "========================================"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Started: $(date)"
echo ""

# Change to project directory
cd /home/<username>/Code/FRESCO-Pipeline

# Create directories
mkdir -p logs
mkdir -p /depot/<group>/data/josh/FRESCO/chunks-v3/manifests
mkdir -p /depot/<group>/data/josh/FRESCO/chunks-v3/validation
mkdir -p /depot/<group>/data/josh/FRESCO/chunks-v3/logs

# Activate conda environment
source ~/anaconda3/bin/activate fresco_v2

# Verify environment
echo "Python version: $(python --version)"
echo "Conda env: $CONDA_DEFAULT_ENV"
echo ""

# Run production build
python build_production_v3.py --config production_v3.json

exit_code=$?

echo ""
echo "========================================"
echo "Completed: $(date)"
echo "Exit code: $exit_code"
echo "========================================"

exit $exit_code

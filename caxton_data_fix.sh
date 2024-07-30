#!/bin/bash
#SBATCH --job-name=caxton_data_fix
#SBATCH --output=caxton_data_fix_%j.out
#SBATCH --error=caxton_data_fix_%j.err
#SBATCH --time=6:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G

# Load required modules
module load python/3.12.1

# Activate virtual environment 
source /home/jadhaiza/miniconda3/bin/activate ka

# Change to the directory containing the script
cd /home/jadhaiza/projects/3D-Printer-Error-Detection/

# Run the Python script
python /home/jadhaiza/projects/3D-Printer-Error-Detection/caxton_data_fix.py

# Deactivate virtual environment
deactivate
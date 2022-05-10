#!/bin/bash
#SBATCH -J Data_acquisition
#SBATCH -p general
#SBATCH -n 1
#SBATCH --output=Data_acquisition_%j.out
#SBATCH --error=Data_acquisition_%j.err
#SBATCH --mail-user=jorge.munoz.s@ug.uchile.cl
#SBATCH --mail-type=ALL

python3 Download_pdb.py
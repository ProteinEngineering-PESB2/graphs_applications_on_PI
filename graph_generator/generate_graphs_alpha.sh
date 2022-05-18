#!/bin/bash
#SBATCH -J generate_graphs_alpha
#SBATCH -p general
#SBATCH -n 1
#SBATCH --mem-per-cpu=16384
#SBATCH --output=generate_graphs_alpha%j.out
#SBATCH --error=generate_graphs_alpha%j.err
#SBATCH --mail-user=jorge.munoz.s@ug.uchile.cl
#SBATCH --mail-type=ALL

python3 Main.py Parametros_alpha.json
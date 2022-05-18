#!/bin/bash
#SBATCH -J generate_graphs_atoms
#SBATCH -p general
#SBATCH -n 1
#SBATCH --mem-per-cpu=16384
#SBATCH --output=generate_graphs_atoms%j.out
#SBATCH --error=generate_graphs_atoms%j.err
#SBATCH --mail-user=jorge.munoz.s@ug.uchile.cl
#SBATCH --mail-type=ALL

python3 Main.py Parametros_atoms.json
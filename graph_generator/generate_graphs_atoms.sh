#!/bin/bash
#SBATCH -J generate_graphs_atoms
#SBATCH -p largemem
#SBATCH -n 1
#SBATCH --output=generate_graphs_atoms%j.out
#SBATCH --error=generate_graphs_atoms%j.err
#SBATCH --mail-user=jorge.munoz.s@ug.uchile.cl
#SBATCH --mail-type=ALL

python3 Main.py Parametros_atoms.json
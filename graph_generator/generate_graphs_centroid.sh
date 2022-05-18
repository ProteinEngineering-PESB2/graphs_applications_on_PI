#!/bin/bash
#SBATCH -J generate_graphs_centroid
#SBATCH -p general
#SBATCH -n 1
#SBATCH --mem-per-cpu=16384
#SBATCH --output=generate_graphs_centroid%j.out
#SBATCH --error=generate_graphs_centroid%j.err
#SBATCH --mail-user=jorge.munoz.s@ug.uchile.cl
#SBATCH --mail-type=ALL

python3 Main.py Parametros_centroid.json
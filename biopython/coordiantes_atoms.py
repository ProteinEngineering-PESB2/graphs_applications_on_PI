from Bio.PDB import *
import pandas as pd

parser = PDBParser()

structure = parser.get_structure("C011-IOH14612", "./C011-IOH14612_renumbered_0001_full_0001.pdb")

df = pd.DataFrame(columns=["atom","x","y","z"])

for atom in structure.get_atoms():
    df2 = {
        "atom": atom.id,
        "x": atom.coord[0],
        "y": atom.coord[1],
        "z": atom.coord[2]
    }

    df = df.append(df2, ignore_index=True)

print(df)

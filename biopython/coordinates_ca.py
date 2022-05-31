from Bio.PDB import PDBParser
import pandas as pd

parser = PDBParser()

structure = parser.get_structure("C011-IOH14612", "./C011-IOH14612_renumbered_0001_full_0001.pdb")

residues = [r for r in structure.get_residues()]

df = pd.DataFrame(columns=["residue","x","y","z"])

for i in range(len(residues)):
    residue_name = residues[i].get_resname()
    coords = residues[i]["CA"].get_coord()
    
    x = coords[0]
    y = coords[1]
    z = coords[2]

    df2 = {
        "residue": residue_name,
        "x": x,
        "y": y,
        "z": z
    }

    df = df.append(df2, ignore_index=True)

print(df)

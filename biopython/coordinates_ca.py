from Bio.PDB import PDBParser
import pandas as pd
import os

parser = PDBParser()

for complex in os.listdir("./results"):
    split_complex = complex.split(".")
    structure = parser.get_structure(split_complex[0], f"./results/{complex}")

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

    df.to_csv(f"./carbonos_alfa/{split_complex[0]}.csv", index=False, header=True)

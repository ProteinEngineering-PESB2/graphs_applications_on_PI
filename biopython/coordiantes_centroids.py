from Bio.PDB import PDBParser
import pandas as pd
import os

parser = PDBParser()

for complex in os.listdir("./results"):
    split_complex = complex.split(".")
    structure = parser.get_structure(split_complex[0], f"./results/{complex}")

    df = pd.DataFrame(columns=["residue","x","y","z"])

    for model in structure:
        for chain in model:
            for residue in chain:
                centroid_x = 0
                centroid_y = 0
                centroid_z = 0

                total = 0

                for atom in residue:
                    x = atom.get_coord()[0]
                    y = atom.get_coord()[1]
                    z = atom.get_coord()[2]

                    centroid_x += x
                    centroid_y += y
                    centroid_z += z

                    total += 1
                
                centroid_x = centroid_x / total
                centroid_y = centroid_y / total
                centroid_z = centroid_z / total
            
                df2 = {
                    "residue": residue.get_resname(),
                    "x": centroid_x,
                    "y": centroid_y,
                    "z": centroid_z
                }

                df = df.append(df2, ignore_index=True)

    df.to_csv(f"./centroids/{split_complex[0]}.csv", index=False, header=True)

                
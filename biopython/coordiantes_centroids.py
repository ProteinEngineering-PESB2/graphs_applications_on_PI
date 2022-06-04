from Bio.PDB import PDBParser
import pandas as pd
import os
import shutil

if os.path.isdir("./centroids"):
    shutil.rmtree("./centroids")

os.mkdir("./centroids")

parser = PDBParser()

cont = 0
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

                residue_name = residue.get_resname()
                residue = ""

                if residue_name == "ALA":
                    residue = "A"
                if residue_name == "ARG":
                    residue = "R"
                if residue_name == "ASN":
                    residue = "N"
                if residue_name == "ASP":
                    residue = "D"
                if residue_name == "CYS":
                    residue = "C"
                if residue_name == "GLN":
                    residue = "Q"
                if residue_name == "GLU":
                    residue = "E"
                if residue_name == "GLY":
                    residue = "G"
                if residue_name == "HIS":
                    residue = "H"
                if residue_name == "ISO":
                    residue = "I"
                if residue_name == "LEU":
                    residue = "L"
                if residue_name == "LYS":
                    residue = "K"
                if residue_name == "MET":
                    residue = "M"
                if residue_name == "PHE":
                    residue = "F"
                if residue_name == "PRO":
                    residue = "P"
                if residue_name == "SER":
                    residue = "S"
                if residue_name == "THR":
                    residue = "T"
                if residue_name == "TRY":
                    residue = "W"
                if residue_name == "TYR":
                    residue = "Y"
                if residue_name == "VAL":
                    residue = "V"
            
                df2 = {
                    "residue": residue,
                    "x": centroid_x,
                    "y": centroid_y,
                    "z": centroid_z
                }

                df = df.append(df2, ignore_index=True)

    df.to_csv(f"./centroids/{split_complex[0]}.csv", index=True, header=True)

    cont += 1
    if cont == 5:
        break

                
from Bio.PDB import PDBParser
import pandas as pd
import os
import shutil

if os.path.isdir("./carbonos_alfa"):
    shutil.rmtree("./carbonos_alfa")

os.mkdir("./carbonos_alfa")

parser = PDBParser()

cont = 0

for complex in os.listdir("./results"):
    split_complex = complex.split(".")
    structure = parser.get_structure(split_complex[0], f"./results/{complex}")

    residues = [r for r in structure.get_residues()]

    df = pd.DataFrame(columns=["residue","x","y","z"])

    for i in range(len(residues)):
        residue_name = residues[i].get_resname()
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


        coords = residues[i]["CA"].get_coord()
        
        x = coords[0]
        y = coords[1]
        z = coords[2]

        df2 = {
            "residue": residue,
            "x": x,
            "y": y,
            "z": z
        }

        df = df.append(df2, ignore_index=True)

    df.to_csv(f"./carbonos_alfa/{split_complex[0]}.csv", index=True, header=True)

    cont += 1

    if cont == 10:
        break
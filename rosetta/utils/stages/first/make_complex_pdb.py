import os

from pymol import cmd

def make_complex_pdb(row, complex_name):
    try:
        filename_antigen = row[1].replace(".pdb", "_repaired.pdb")
        filename_antibody_HC = row[4].replace(".pdb", "_repaired.pdb")
        filename_antibody_LC = row[7].replace(".pdb", "_repaired.pdb")

        cmd.load(os.path.join(row[0], filename_antigen))
        cmd.load(os.path.join(row[0], filename_antibody_HC))
        cmd.load(os.path.join(row[0], filename_antibody_LC))
        cmd.select("complex", "all")
        cmd.save(os.path.join(row[0], f"{complex_name}.pdb"), "complex", -1, "pdb")
        cmd.reinitialize()

        return True
    except:
        return False
import os

from pymol import cmd

def change_chains_antibodies(row):
    try:
        structure_align = os.path.join(os.getcwd(), "utils", "1bey.pdb")

        antibody_HC_data = row[4:7]
        antibody_LC_data = row[7:11]
        
        new_row = [antibody_HC_data, antibody_LC_data]

        structure_align = structure_align.replace("\n", "")

        for element in new_row:
            name_file_load = element[0].replace(".pdb", "_repaired.pdb")
            cmd.load(os.path.join(row[0], name_file_load))
            filename = name_file_load.replace(".pdb", "")
            cmd.alter("(chain " + element[1] + ")", "chain ='" + element[2] + "'")
            cmd.load(structure_align)
            file_pattern=structure_align.split("/")[-1].replace(".pdb", "")
            cmd.align(filename, file_pattern)
            cmd.drag(filename)
            cmd.save(os.path.join(row[0], element[0].replace(".pdb", "_repaired.pdb")), filename, -1, "pdb")
            cmd.reinitialize()

        return True
    except:
        return False

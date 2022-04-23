import os

from pdbfixer import PDBFixer
from openmm.app import PDBFile


def repair_pdb_to_complex(row):
    try:
        antigen_data = row[1:4]
        antibody_HC_data = row[4:7]
        antibody_LC_data = row[7:11]

        new_row = [antigen_data, antibody_HC_data, antibody_LC_data]

        for element in new_row:
            fixer = PDBFixer(filename=os.path.join(row[0], element[0]))
            filename = element[0].replace(".pdb", "")
            fixer.findMissingResidues()
            fixer.findNonstandardResidues()
            fixer.replaceNonstandardResidues()
            fixer.removeHeterogens(True)
            fixer.findMissingAtoms()
            fixer.addMissingAtoms()
            fixer.addMissingHydrogens(7.0)
            PDBFile.writeFile(fixer.topology, fixer.positions, open(
                os.path.join(row[0], f"{filename}_repaired.pdb"), "w"))

        return True
    except:
        return False

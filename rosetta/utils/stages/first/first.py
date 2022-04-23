import os
import shutil
import subprocess

from .get_antigen_chain import get_antigen_chain
from .repair_pdb_to_complex import repair_pdb_to_complex
from .change_chains_antibodies import change_chains_antibodies
from .make_complex_pdb import make_complex_pdb
from .renumber_chains import renumber_chains
from .erase_temp_files import erase_temp_files
from .make_repack_options_file import make_repack_options_file

from stages.second import second
from stages.third import third
from stages.fourth import fourth
from stages.fifth import fifth

def first(antibody, antigen, antigen_pdb, antigen_chain, rosetta_path):
    antibody_HC_path = os.path.join(
        os.getcwd(), "antibodies", f"{antibody}_HC.pdb")
    antibody_LC_path = os.path.join(
        os.getcwd(), "antibodies", f"{antibody}_LC.pdb")

    if not ((os.path.isfile(antibody_HC_path)) and (os.path.isfile(antibody_LC_path))):
        return False

    antigen_pdb_path = os.path.join(os.getcwd(), "antigens", antigen_pdb)
    if not os.path.isfile(antigen_pdb_path):
        return False

    antigen_split = antigen.split(":")
    if len(antigen_split) == 3:
        complex_folder = os.path.join(
            os.getcwd(), "results", f"{antibody}-{antigen_split[2]}")
        os.mkdir(complex_folder)

        shutil.copyfile(antibody_HC_path, os.path.join(
            complex_folder, f"{antibody}_HC.pdb"))
        shutil.copyfile(antibody_LC_path, os.path.join(
            complex_folder, f"{antibody}_LC.pdb"))
        shutil.copyfile(antigen_pdb_path, os.path.join(
            complex_folder, f"{antigen_pdb}"))

        result = get_antigen_chain(
            antigen_pdb=antigen_pdb, antigen_chain=antigen_chain, complex_folder=complex_folder)

        if result == False:
            return False
        
        row = [complex_folder, antigen_pdb, antigen_chain, "A",
            f"{antibody}_HC.pdb", "A", "H", f"{antibody}_LC.pdb", "A", "L"]

        result = repair_pdb_to_complex(row=row)

        if result == False:
            return False
        
        result = change_chains_antibodies(row=row)

        if result == False:
            return False

        result = make_complex_pdb(row=row, complex_name=f"{antibody}-{antigen_split[2]}")

        if result == False:
            return False

        result = renumber_chains(row=row, complex_name=f"{antibody}-{antigen_split[2]}")

        if result == False:
            return False
        
        erase_temp_files(row=row, complex_name=f"{antibody}-{antigen_split[2]}")

        make_repack_options_file(row=row, antibody=antibody, antigen=antigen_split[2])

        # STAGE TWO
        second.main(complex_folder=row[0], rosetta_path=rosetta_path)

        # STAGE THREE
        result = third.main(complex_folder=row[0], antibody=antibody, antigen=antigen_split[2], rosetta_path=rosetta_path)

        if result == False:
            return False
        
        fourth.main(complex_folder=row[0], rosetta_path=rosetta_path)

        result = fifth.main(complex_folder=row[0])

        if result == False:
            return False
    else:
        return False


    return True

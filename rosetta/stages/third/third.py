import os
import re

from utils.create_file import create_file
from .process_results_repack import process_results_repack
from .make_protocol_docking import make_protocol_docking
from .make_docking_options import make_docking_options

def main(complex_folder, antibody, antigen, rosetta_path):
    result = process_results_repack(complex_folder=complex_folder, antibody=antibody, antigen=antigen, rosetta_path=rosetta_path)
    
    if result == False:
        return False
    
    make_protocol_docking(complex_folder=complex_folder, structure_selected=result)

    make_docking_options(complex_folder=complex_folder, structure_selected=result)

    
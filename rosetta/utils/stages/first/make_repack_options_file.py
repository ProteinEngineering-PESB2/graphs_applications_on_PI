import os

from utils.create_file import create_file

def make_repack_options_file(row, antibody, antigen):
    path_pdb = os.path.join(row[0], f"{antibody}-{antigen}_renumbered.pdb")

    content = f"-in:file:fullatom\n-out:file:fullatom\n-s {path_pdb}\n-linmem_ig 10\n-ex1\n-ex2\n-use_input_sc\n-score:weights talaris2014.wts\n-out:file:scorefile repack.fasc\n-out:path:all {row[0]}/"
    create_file("repack2.options", content, row[0])
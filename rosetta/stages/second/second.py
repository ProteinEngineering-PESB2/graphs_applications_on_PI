import os
import subprocess

def main(complex_folder, rosetta_path):
    repack_options = os.path.join(complex_folder, "repack2.options")

    #/home/claudio/tesis/rosetta_src_2021.16.61629_bundle/main/source/bin/rosetta_scripts.linuxgccrelease
    subprocess.run([f"{rosetta_path}/source/bin/rosetta_scripts.linuxgccrelease", f"@{repack_options}", "-parser:protocol", "./repack2.xml", "-corrections::restore_talaris_behavior", "True", "-nstruct", "1"])
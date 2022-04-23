import os
import subprocess

def main(complex_folder, rosetta_path):
    docking_new_options = os.path.join(complex_folder, "docking_new.options")
    docking_full3 = os.path.join(complex_folder, "docking_full3.xml")
    
    subprocess.run([f"{rosetta_path}/source/bin/rosetta_scripts.linuxgccrelease", f"@{docking_new_options}", "-parser:protocol", f"{docking_full3}", "-out:suffix", "_full", "-corrections::restore_talaris_behavior", "True", "-nstruct", "1"])
import os
import shutil

for complex in os.listdir(f"./results"):
    shutil.move(f"./results/{complex}", f"./results/{complex}.pdb")
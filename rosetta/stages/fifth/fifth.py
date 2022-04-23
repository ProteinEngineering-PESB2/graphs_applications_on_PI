import os
import re

def main(complex_folder):
    docking_selected=""

    path_docking = os.path.join(complex_folder, "docking2.fasc")

    if not os.path.isfile(path_docking):
        return False

    scoring_file_docking = os.path.join(complex_folder, "docking2.fasc")
    
    file_results = open(scoring_file_docking, "r").read().splitlines()[2:]
    score = 0
    i_sc = -5
    for line in file_results:
        results= re.sub(' +', ' ',line).split(" ")
        if float(results[1]) < score and float(results[5]) < i_sc and float(results[5]) > -10:
            docking_selected=results[-1]
            score= float(results[1])
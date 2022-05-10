from distance_graph_generator import *
from tqdm import tqdm
import os
import json
import sys

def Main(main_folder, granularity, lower, upper, check_protein, dist):
    categories = os.listdir(main_folder)
    errors = dict()

    for structure in categories:
        sub_folder = main_folder + '/' + structure
        if os.path.isdir(sub_folder):
            pdb_list = [pdb for pdb in os.listdir(sub_folder) if pdb.endswith('.pdb')]
            errors_list = []

            for pdb in tqdm(pdb_list):
                try:
                    pdb_to_distance_graph(pdb, granularity, dist, lower, upper, sub_folder, check_protein)
                except:
                    errors_list.append(pdb)

            errors[sub_folder] = errors_list

    # Save files
    with open(main_folder + '/Graph_' + granularity +'_errors.json', 'w') as fp:
        json.dump(errors, fp)


if __name__ == "__main__":

    param = {"Folder": "", 
            "Distance": "euclidean", 
            "Granularity": "alpha_carbon",
            "Lower": 2, 
            "Upper": 15, 
            "Only_proteins": True}
    
    Allowed_granularities = ['alpha_carbon', 'centroid', 'atoms']

    if len(sys.argv) != 1:
        file = open(sys.argv[1])
        param_news = json.load(file)
        param.update(param_news)

    if not param['Granularity'] in Allowed_granularities:
        print('Granularidad no valida')
        sys.exit()

    Main(param['Folder'], param['Granularity'], param['Lower'], param['Upper'], 
         param['Only_proteins'], param['Distance'])

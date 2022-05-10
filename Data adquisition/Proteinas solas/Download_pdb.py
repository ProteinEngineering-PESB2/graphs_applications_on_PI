""" Script para descargar los archivos pdb desde una lista presentada
en un json
"""
# Importing libraries
import urllib.request
import json
import os, errno
import random
from tqdm import tqdm

# Choosing the Seed
random.seed(100)

# Download pdb files from url (Funcion adquirida desde script whati_services_all.py)
def dowload_pdb_code(pdb_code, input_folder=""):

    response = 0
    try:
        url_data = "http://files.rcsb.org/download/{}.pdb".format(pdb_code)

        if input_folder == "":
            pdb_file = "{}.pdb".format(pdb_code)
        else:
            pdb_file = "{}/{}.pdb".format(input_folder, pdb_code)

        urllib.request.urlretrieve(url_data, pdb_file)
    except:
        response = -1
        pass

    return response


def create_folder(name):
    try:
        os.makedirs(name)

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


if  __name__ == "__main__":
    # Open file
    with open("Resultados_sin_multiclase.json") as file:
        pdb_list = json.load(file)

    # Parameters
    main_folder = "PROTEINS"
    sample_size = 1500

    create_folder(main_folder)

    # Create dict to save samples
    sample = dict()
    errors = dict()

    for category in pdb_list.keys():
        cat_name = category
        errors_list = []

        if category == "Alpha and beta proteins (a/b)":
            cat_name = "Alpha and beta proteins (a_b)"

        # Create folder with the name of the category
        create_folder(main_folder + "/" + cat_name)
        folder = main_folder + "/" + cat_name
        
        # Select subset
        if len(pdb_list[category]) < sample_size:
            sub_set = random.sample(pdb_list[category], len(pdb_list[category]))
        else:
            sub_set = random.sample(pdb_list[category], sample_size)
        
        sample[category] = sub_set

        # Download the pdb in the appropriate folder
        for pdb in tqdm(sub_set):
           response = dowload_pdb_code(pdb, folder)
           if response == -1:
               errors_list.append(pdb)

        errors[category] = errors_list


    # Save files
    with open(main_folder + '/Sample.json', 'w') as fp:
        json.dump(sample, fp)

    with open(main_folder + '/Errors.json', 'w') as fp:
        json.dump(errors, fp)
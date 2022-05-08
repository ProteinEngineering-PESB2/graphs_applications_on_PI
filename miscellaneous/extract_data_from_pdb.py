import sys
import os
import json

def read_and_extract_data(pdb_document):
    pdb_file_object = open(pdb_document, 'r')
    line = pdb_file_object.readline()

    line_reads = []
    while line:
        line = line.replace("\n", "")
        if "KEYWDS" in line:
            line_reads.append(line.strip().split("KEYWDS")[1].strip())
        line = pdb_file_object.readline()

    pdb_file_object.close()

    return line_reads

#recibe un directorio donde se encuentran los pdb
pdb_path = sys.argv[1]

#obtenemos todos los pdb en el directorio
list_pdb = os.listdir(pdb_path)

dict_data = {}

for pdb_file in list_pdb:
    code_pdb = pdb_file.split(".")[0].upper()
    print("Process PDB: ", pdb_file)
    pdb_file = pdb_path+pdb_file
    lines_in_pdb = read_and_extract_data(pdb_file)
    dict_data.update({code_pdb: lines_in_pdb})

print("Export data")
name_export = "dic_keywords_pdb_process.json"
with open(name_export, 'w') as export_data:
    json.dump(dict_data, export_data)


"""Encuentra los elementos comunes en el archivo Resultados.json
"""
# Importing libraries
import json

def intersectar(lista1, lista2):
    """_summary_

    Args:
        lista1 (_type_): _description_
        lista2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    set1 = set(lista1)
    set2 = set(lista2)
    return list(set1.intersection(set2))

if  __name__ == "__main__":
    # Open file
    with open("Resultados.json") as file:
        pdb_list = json.load(file)
    
    keys = list(pdb_list.keys())
    multiclase = dict()
    
    for i in range(len(keys)):
        multiclase.update({keys[i]:{}})
    
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            interseccion = intersectar(pdb_list[keys[i]],
                                    pdb_list[keys[j]])
            multiclase[keys[i]].update({keys[j]: interseccion})
            multiclase[keys[j]].update({keys[i]: interseccion})

with open('Multiclass.json', 'w') as fp:
    json.dump(multiclase, fp)
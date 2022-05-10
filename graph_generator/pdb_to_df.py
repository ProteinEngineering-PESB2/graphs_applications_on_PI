"""Script that generates a graph in gpickle format and a adjacency list in
csv format from a pdb file.
"""
# Importing libraries
from Bio.PDB import PDBParser
import pandas as pd

def name_atom(atom):

    name = atom.get_name()
    res = atom.get_parent()
    res_name = res.get_resname() + str(res.id[1])
    chain = atom.get_parent().get_parent().id
    return name+'_'+res_name+'_'+chain


def name_centroid(residue):

    name = residue.get_resname() + str(residue.id[1])
    chain = residue.get_parent().id
    return 'Cent_'+name+'_'+chain


def estimate_centroid(residue):

    vector = [0, 0, 0]
    atoms_list = list(residue.get_atoms())

    for atom in atoms_list:
        position = atom.get_vector()
        vector[0] += position[0]
        vector[1] += position[1]
        vector[2] += position[2]
    
    return [i/len(atoms_list) for i in vector]


def append_atom(atom, matrix):
    
    vector = atom.get_vector()
    vector = [value for value in vector]
    row_value = [name_atom(atom)] + vector
    matrix.append(row_value)

    return matrix


def is_aminoacid(res):
    '''Revisa si el elemento en cuestion es parte
    de un aminoacido.

    Parametros:
    res  -- String
            Nombre del residuo al que pertenece el elemento
            a estudiar.

    Retorna:
            Boolean
            True si corresponde a un elemento perteneciente
            a un aminoacido, False si no.
    '''

    Allowed_aa = ['GLY', 'ALA', 'VAL', 'LEU', 'ILE', 'PHE', 'TYR', 'TRP',
                  'SER', 'THR', 'CYS', 'MET', 'PRO', 'ASP', 'GLU', 'ASN',
                  'GLN', 'LYS', 'ARG', 'HIS']
    
    return res in Allowed_aa


# Reading the pdb file
def process_pdb_as_df(pdb_name, granularity, check_protein = True):
    matrix_data = []
    
    # Read the pdb file
    sloppyparser = PDBParser(PERMISSIVE=True)
    structure = sloppyparser.get_structure('protein', pdb_name)
    model = structure[0]
    residues = list(model.get_residues())

    # Name of the pdb
    name = granularity + "_" + pdb_name[-8:-4]

    # Obtain the coord according the granularity
    if granularity == "alpha_carbon":
        if check_protein:
            for i in range(len(residues)):
                if is_aminoacid(residues[i].get_resname()):
                    try:
                        residues[i]['CA']
                    except:
                        pass
                    else:
                        matrix_data = append_atom(residues[i]['CA'], matrix_data)
        else:
            for i in range(len(residues)):
                    try:
                        residues[i]['CA']
                    except:
                        pass
                    else:
                        matrix_data = append_atom(residues[i]['CA'], matrix_data)

    elif granularity == "centroid":
        if check_protein:
            for i in range(len(residues)):
                if is_aminoacid(residues[i].get_resname()):
                    vector = estimate_centroid(residues[i])
                    row_value = [name_centroid(residues[i])] + vector
                    matrix_data.append(row_value)
        else:
            for i in range(len(residues)):
                vector = estimate_centroid(residues[i])
                row_value = [name_centroid(residues[i])] + vector
                matrix_data.append(row_value)

    elif granularity == 'atoms':
        if check_protein:
            for i in range(len(residues)):
                if is_aminoacid(residues[i].get_resname()):
                    atoms = list(residues[i].get_atoms())
                    for j in range(len(atoms)):
                        matrix_data = append_atom(atoms[j], matrix_data)
        else:
            for i in range(len(residues)):
                    atoms = list(residues[i].get_atoms())
                    for j in range(len(atoms)):
                        matrix_data = append_atom(atoms[j], matrix_data)

    df_export = pd.DataFrame(matrix_data, columns=['Node', 'coord1', 'coord2', 'coord3'])
    return (df_export, name)

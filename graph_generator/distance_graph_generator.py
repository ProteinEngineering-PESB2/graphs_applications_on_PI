from pdb_to_df import *
from node_list_generator import *
from distance_estimator import *
from distance_filter import *
from graph_generator import *
import errno
import os

def create_folder(name):
    try:
        os.makedirs(name)

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def pdb_to_distance_graph(pdb_name, granularity, dist, lower, upper, input_folder, check_protein):

    pdb = input_folder + '/' + pdb_name[0:-4]

    # Decompress pdb file
    try:
        with ZipFile(pdb + '.zip') as file:
            file.extractall(input_folder)
    
    # If is already decompressed not do anything
    except:
        pass

    pdb = pdb + '.pdb'

    # Read the pdb file
    coords, name = process_pdb_as_df(pdb, granularity, check_protein)

    # Create node list
    print('Creando lista de nodos')
    path = input_folder + '/Node_lists'
    create_folder(path)
    generate_node_list(coords, name, path)

    # Generate distance adjacency list
    print('Creando lista de distancias')
    path = input_folder + '/Distance_list'
    create_folder(path)
    distance_list = path + '/' + "distance_list_" + name + ".csv"
    process_parallel_distance(coords, distance_list)

    # Filter the distances
    print('Filtrando lista de distancias')
    path = input_folder + '/Distance_list/Filtered'
    create_folder(path)
    distance_filtered = path + '/' + dist + "_distance_list_filtered_" + name + ".csv"
    filter_distance(distance_list, lower, upper, dist, distance_filtered)

    # Generate distance graph
    path = input_folder + '/Graphs'
    create_folder(path)

    print('Creando grafo de distancias')
    node_list_name = input_folder + "/Node_lists/" + "node_list_" + name + ".csv"
    graph_name = 'distance_' + dist + '_' + name
    generate_graph(distance_filtered, node_list_name, path, graph_name)

    # Compress files
    with ZipFile(node_list_name[0:-4] + '.zip', 'w') as file:
        file.write(node_list_name, "node_list_" + name + ".csv")

    with ZipFile(distance_list[0:-4] + '.zip', 'w') as file:
        file.write(distance_list, "distance_list_" + name + ".csv")

    with ZipFile(distance_filtered[0:-4] + '.zip', 'w') as file:
        file.write(distance_filtered, dist + "_distance_list_filtered_" + name + ".csv")

    # Remove decompressed files
    os.remove(pdb)
    os.remove(node_list_name)
    os.remove(distance_list)
    os.remove(distance_filtered)

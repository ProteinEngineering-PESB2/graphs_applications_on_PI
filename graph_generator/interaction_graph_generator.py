from whati_service_all import *
from process_interactions import *
from graph_generator import *
import errno
import os

def create_folder(name):
    try:
        os.makedirs(name)

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def pdb_to_interaction_graph(pdb_name, input_folder, node_list_name):

    # Generate interactions adjacency 
    interaction_list_name = input_folder + '/Interaction_list' + '/' + 'interactions_list_' + pdb_name[-8:-4] + '.csv'

    print('Creando lista de interacciones')
    input_folder = "{}/".format(input_folder)
    dict_response = {}

    response_interactions = run_process_service(input_folder, pdb_name)
    dict_response.update({"response_service":response_interactions})

    path = input_folder + '/Interaction_list'
    create_folder(path)
    process_interactions(dict_response, path, pdb_name[-8:-4])

    # Generate interactions graph
    print('Creando grafo de interacciones')
    graph_name = 'interactions_' + pdb_name[-8:-4]
    path = input_folder + '/Graphs'
    generate_graph(interaction_list_name, node_list_name, path, graph_name)
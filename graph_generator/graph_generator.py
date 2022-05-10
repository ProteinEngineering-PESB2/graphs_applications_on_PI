# Importing libraries
import pandas as pd
import json
import networkx as nx
import numpy as np
import sys, getopt
import textwrap
import os.path


def generate_graph(adjaceny_file, nodes_file, path, name):
    '''Crea una grafo a partir de una lista de adyacencia,
    considerando un limite superior para los pesos. En el 
    caso de que se usen interacciones como pesos se recomienda
    considerarlas todas, es decir, utilizar la opcion percentil
    con un porcentaje de 100.

    Parametros:
    adjaceny_file  -- String
                      Nombre del archivo que posee la lista de adjacencia.
    nodes_file     -- String
                      Nombre del archivo que posee la lista de nodos.
    path           -- String
                      Path para guardar el archivo.

    Retorna:
            None
            Genera archivo gpickle con el grafo.
    '''
    # Reading the adjacency list with pandas
    df_edges = pd.read_csv(adjaceny_file, header=0)

    # Reading the node list with pandas
    df_nodes = pd.read_csv(nodes_file, header=0)

    # Creating graph
    graph = nx.Graph()

    # Adding nodes
    for index, row in df_nodes.iterrows():
        graph.add_node(row['Node'])

    # Adding edges
    for index, row in df_edges.iterrows():
        graph.add_edge(row['Node_1'], row['Node_2'], weight=row['Weight'])

    file_name = path + '/graph_' + name

    nx.write_gpickle(graph, file_name + '.gpickle')

    # Create json that save statistics
    Info = {'File_name': file_name,
            'Nodes': graph.number_of_nodes(),
            'Edges': graph.number_of_edges()}

    # Saving json
    with open(file_name + '.json', 'w') as fp:
        json.dump(Info, fp)

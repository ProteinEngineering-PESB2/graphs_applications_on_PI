# Importing libraries
from Bio.PDB import PDBParser
import numpy as np
import pandas as pd
import json
import os.path
import multiprocessing as mp
import json 
import time 
from scipy.spatial import distance


def process_config_file(config_file):

    with open(config_file) as params:
        dict_params = json.load(params)
    
    return dict_params

def create_vector_values(dataset, index):

	#hacerlo con pandas para mas facilidad
	row =  [dataset[value][index] for value in dataset.keys()]
	return row

def paralelism_create_vector_distance(dataset, start, stop, record_vectors):

	for i in range(start, stop):#completo		
		vector1 = create_vector_values(dataset, i)
		record_vectors.append(vector1)

def estimated_distance(row1, row2):

    name_node_1 = row1[0]
    name_node_2 = row2[0]
    euclidean = distance.euclidean(row1[1:], row2[1:])
    cosine = distance.cosine(row1[1:], row2[1:])
    manhattan = distance.cityblock(row1[1:], row2[1:])
    
    return [name_node_1, name_node_2, euclidean, cosine, manhattan]

def estimated_distance_multi(vector1, matrix_vector):

	distance_results = []

	for vector in matrix_vector:
		distance_value = estimated_distance(vector1, vector)
		distance_results.append(distance_value)

	return distance_results

def function_to_estimate_distances(dataset, vector_list, start, stop, records_distances):

	print("Start: ", os.getpid())
	for vector1 in vector_list:
		distance_value = estimated_distance_multi(vector1, vector_list[start:stop])
		records_distances.append(distance_value)

	print("Finish: ", os.getpid())

def process_parallel_distance(dataset, name_output):

    #get number of cpu
    cpu_number = mp.cpu_count()
    print(cpu_number)

    #make ranges between all elements
    number_data = int(len(dataset)/cpu_number)
    rest_element = int(len(dataset)%cpu_number)

    #get index
    index_data = []

    for i in range(cpu_number):
        start = i*number_data
        stop = start+number_data

        if i == cpu_number-1:
            stop = stop+rest_element
        row = [start, stop]
        index_data.append(row)
    
    #star paralelism
    with mp.Manager() as manager:
        
        record_vectors = manager.list([])
        records_distances = manager.list([])

        processes_create_vectors = []
        processes_estimated_distance = []

        print("Init process")
        
        for i in range(cpu_number):

            #create vector list (for 1)
            start = index_data[i][0]
            stop = index_data[i][1]
            print(start, stop)

            #paralelize todos los vectores 01
            processes_create_vectors.append(mp.Process(target=paralelism_create_vector_distance, args=[dataset, start, stop, record_vectors]))
        
        #run and join data process	
        for p in processes_create_vectors:
            print("Start process create vectors")
            p.start()

        for p in processes_create_vectors:
            print("Join data create vectors process")
            p.join()
        
        print(len(record_vectors))

        time.sleep(10)

        for i in range(cpu_number):

            start = index_data[i][0]
            stop = index_data[i][1]
            print(start, stop)

            processes_estimated_distance.append(mp.Process(target=function_to_estimate_distances, args=[dataset, record_vectors, start, stop, records_distances]))

        for p in processes_estimated_distance:
            print("Start process estimated distance")
            p.start()

        for p in processes_estimated_distance:
            print("Process data join estimated distance")
            p.join()
        
        #export data distances
        print("Export results")
        matrix_data = []
        for record_row in records_distances:
            for record in record_row:
                row = [value for value in record]
                matrix_data.append(row)

        print(len(matrix_data))

        data_export = pd.DataFrame(matrix_data, columns=["Node_1", "Node_2", "euclidean", "correlation", "cosine"])
        data_export.to_csv(name_output, index=False)

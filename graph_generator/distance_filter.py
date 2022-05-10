# Importing libraries
import pandas as pd
import numpy as np



def filter_distance(File:str, lower:float, upper:float, dist: str, name_output:str) -> None:

    # Reading the adjacency list with pandas
    df_edges = pd.read_csv(File, header=0)
    df_edges = df_edges[df_edges['Node_1'] != df_edges['Node_2']]
    df_edges.dropna(inplace=True)

    # Types of distance
    distance_types = ['euclidean', 'cosine', 'manhattan']

    if dist in distance_types:
        
        # Filtering the values
        df_result = df_edges[['Node_1', 'Node_2', dist]]
        df_result = df_result[df_result[dist] <= upper]
        df_result = df_result[df_result[dist] >= lower]
        df_result = df_result.rename(columns={dist: 'Weight'})

        # Saving the file
        df_result.to_csv(name_output, index=False)

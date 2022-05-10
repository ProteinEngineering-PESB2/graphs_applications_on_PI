# Importing libraries
import pandas as pd
import numpy as np
import sys, getopt
import textwrap
import os.path

def generate_node_list(df, name:str, path:str):

    # Obtaining nodes
    nodes = df['Node'].unique()

    # Generating data frame
    df_node = pd.DataFrame(nodes, columns=['Node'])
    
    # Saving the file
    File_name= path + "/" + "node_list_" + name + ".csv"

    df_node.to_csv(File_name, index=False)

import pandas as pd

data = pd.read_csv(sep='\t', filepath_or_buffer='../inferred.tsv', names=['node1','node2','val'])

data_nodes = pd.concat([data['node1'], data['node2']], ignore_index=True)

data_nodes = data_nodes.to_frame('id:ID')

data_nodes[':LABEL'] = 'GEN'

data_nodes =  data_nodes.drop_duplicates()

data_nodes.to_csv("nodes_inferred.csv", index=False)
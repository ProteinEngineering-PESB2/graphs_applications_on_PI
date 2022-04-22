import sys
import random
import pandas as pd

#inputs from console data
nodes = int(sys.argv[1])
edges = int(sys.argv[2])
name_export = sys.argv[3]

#creatin nodes
print("Nodes creation")
list_nodes = ["N_{}".format(i) for i in range(1, nodes+1)]

print("Start edges creation")
list_edges = []

for i in range(edges):
    node1 = random.choice(list_nodes)
    node2 = random.choice(list_nodes)
    value = random.uniform(0, 10)

    edge_value = [node1, node2, value]
    list_edges.append(edge_value)

print("Export to csv")
df_export = pd.DataFrame(list_edges, columns=['n1', 'n2', 'val'])
df_export.to_csv(name_export, index=False)
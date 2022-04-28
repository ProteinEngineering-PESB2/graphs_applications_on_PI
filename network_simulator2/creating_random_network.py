from sqlite3 import Row
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

csv_nodes = []
for i in range(0, len(list_nodes)):
    row = [list_nodes[i], 'PROTEIN']
    csv_nodes.append(row)

print("Start edges creation")
list_edges = []

for i in range(edges):
    node1 = random.choice(list_nodes)
    node2 = random.choice(list_nodes)
    value = random.uniform(0, 10)

    edge_value = [node1, value, node2, 'ENLACE' ]
    list_edges.append(edge_value)


print("Export to csv")
df_export = pd.DataFrame(list_edges, columns=[':START_ID', 'val',':END_ID', ':TYPE'])
df_export.to_csv("data/relaciones_n"+sys.argv[1]+".csv", index=False)

df_export_nodos = pd.DataFrame(csv_nodes, columns=['nodo:ID',':LABEL'])
df_export_nodos.to_csv("data/"+name_export+"_n"+sys.argv[1]+".csv", index=False)
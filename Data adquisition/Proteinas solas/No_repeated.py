# Import libraries
import json
import pandas as pd

# Open files
with open("Resultados.json") as file:
    pdb_list = json.load(file)

with open("Multiclass.json") as file:
    repeated = json.load(file)

# Create dict to save the not repeated elements
sub_set = dict()

# Eliminate repeated elements
for key in pdb_list.keys():
    set1 = set(pdb_list[key])
    set2 = set()

    for sub_key in repeated[key].keys():
        set3 = set(repeated[key][sub_key])
        set2 = set2.union(set3)

    no_repeated = list(set1 - set2)
    sub_set[key] = no_repeated

# Save not repeated elements
with open('Resultados_sin_multiclase.json', 'w') as fp:
    json.dump(sub_set, fp)

# Generating a dataframe
df = pd.DataFrame(columns=['All alpha proteins', 'All beta proteins',
                           'Alpha and beta proteins (a+b)', 'Alpha and beta proteins (a/b)',
                           'Small proteins'])

row = {}
total = 0

# Save the total lenght of each category
for SCOP in sub_set.keys():
    contenido = len(sub_set[SCOP])
    total += contenido
    row.update({SCOP: contenido})
    
row.update({'Total': total})
df = df.append(row, ignore_index=True)

# Save file
df.to_excel('Resultado_sin_multiclase_estadisticas.xlsx', index=False)
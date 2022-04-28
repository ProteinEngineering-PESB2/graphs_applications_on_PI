# Importing libraries
import json
import pandas as pd

# Load json
Data = open('Multiclass.json')
Data = json.load(Data)

# Generating a dataframe
df = pd.DataFrame(columns=['Clasificacion', 'All alpha proteins', 'All beta proteins',
                           'Alpha and beta proteins (a+b)', 'Alpha and beta proteins (a/b)',
                           'Small proteins'])


# Categorias
keys = list(Data.keys())

for i in range(len(keys)):
    row = {'Clasificacion': keys[i]}
    total = 0

    for j in range(len(keys)):
        if i != j:
            contenido = len(Data[keys[i]][keys[j]])
            row.update({keys[j]: contenido})
            total += contenido

    row.update({'Total': total})
    df = df.append(row, ignore_index=True)

# Saving file
df.to_excel('Multiclass_estadisticas.xlsx', index=False)



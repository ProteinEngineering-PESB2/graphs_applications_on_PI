# Importing libraries
import json
import pandas as pd

# Load json
Data = open('Resultados.json')
Data = json.load(Data)

# Generating a dataframe
df = pd.DataFrame(columns=['All alpha proteins', 'All beta proteins',
                           'Alpha and beta proteins (a+b)', 'Alpha and beta proteins (a/b)',
                           'Small proteins'])

# Dict to save data
row = {}

total = 0

for SCOP in Data.keys():
    contenido = len(Data[SCOP])
    total += contenido
    row.update({SCOP: contenido})
    
row.update({'Total': total})
df = df.append(row, ignore_index=True)

# Saving file
df.to_excel('Resultado_estadisticas.xlsx', index=False)



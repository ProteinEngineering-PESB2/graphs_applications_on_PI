import json
import os
import Download_pdb as D

# Load json
Data = open('Sample.json')
Data = json.load(Data)

for key in Data.keys():
    print(key, ' = ', len(Data[key]))

comp = os.listdir("PROTEINS/All beta proteins")
for i in range(len(comp)):
    comp[i] = comp[i][0:4]

set1 = set(Data["All beta proteins"])
set2 = set(comp)
set3 = list(set1 - set2)
print(set3)
print(D.dowload_pdb_code(set3[0]))



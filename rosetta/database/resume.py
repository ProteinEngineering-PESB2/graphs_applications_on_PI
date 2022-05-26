import pymongo
import pandas as pd

df = pd.read_csv("./antigen_antibody_interactions.csv")

myclient = pymongo.MongoClient("mongodb+srv://claudio:claudio123@rosetta-tesis.n97zj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

mydb = myclient["complex-rosetta"]

mycol = mydb["complexs"]

cont_0 = 0
cont_1 = 0
cont_2 = 0
for complex in mycol.find({"success": True, "executed": True}):
    antibody = complex["antibody"]
    antigen = complex["antigen"]

    interaction = df["category_full_space"][df["antibody"] == antibody][df["antigen"] == antigen].values
    if (len(interaction) == 1):
        if (interaction[0] == 0): cont_0 += 1
        if (interaction[0] == 1): cont_1 += 1
        if (interaction[0] == 2): cont_2 += 1

print("Total de complejos:", mycol.count_documents({}))
print("Total de complejos ejecutados:", mycol.count_documents({"executed": True}))
print("Total de complejos ejecutados y que funcionaron:", mycol.count_documents({"executed": True, "success": True}))
print("Complejos con interacción 0: ", cont_0)
print("Complejos con interacción 1: ", cont_1)
print("Complejos con interacción 2: ", cont_2)
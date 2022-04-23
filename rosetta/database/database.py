import pymongo
import pandas as pd

myclient = pymongo.MongoClient("mongodb+srv://claudio:claudio123@rosetta-tesis.n97zj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

mydb = myclient["complex-rosetta"]

mycol = mydb["complexs"]

data = pd.read_csv("../datasets/antigen_antibody_interactions.csv")

for i in range(len(data)):
    mydict = {
        "antibody": data["antibody"].iloc[i],
        "antigen": data["antigen"].iloc[i],
        "executed": False,
        "success": False
    }

    mycol.insert_one(mydict)
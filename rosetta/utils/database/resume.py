import pymongo

myclient = pymongo.MongoClient("mongodb+srv://claudio:claudio123@rosetta-tesis.n97zj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

mydb = myclient["complex-rosetta"]

mycol = mydb["complexs"]

print("Total de complejos:", mycol.count_documents({}))
print("Total de complejos ejecutados:", mycol.count_documents({"executed": True}))
print("Total de complejos ejecutados y que funcionaron:", mycol.count_documents({"executed": True, "success": True}))
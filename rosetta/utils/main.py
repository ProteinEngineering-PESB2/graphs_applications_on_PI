import os
import pymongo
import argparse

import pandas as pd

from stages.first.first import first


def main():
    # Creamos la carpeta donde almacenaremos los complejos.
    results_directory = os.path.join(os.getcwd(), './results')

    myclient = pymongo.MongoClient(
        "mongodb+srv://claudio:claudio123@rosetta-tesis.n97zj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    mydb = myclient["complex-rosetta"]

    mycol = mydb["complexs"]

    if not os.path.isdir(results_directory):
        os.mkdir(results_directory)

    # Leemos el datasets que resumen todas las interacciones antígeno-anticuerpo.
    df = pd.read_csv(os.path.join(
        os.getcwd(), "./datasets/antigen_antibody_interactions.csv"))

    parser = argparse.ArgumentParser(description="Rosetta")
    parser.add_argument("--p", help="Path of rosetta")
    parser.add_argument("--n", help="Number of models")

    args = parser.parse_args()

    rosetta_path = args.p
    rosetta_models = args.n

    for i in range(int(rosetta_models)):
        element = mycol.aggregate([
            {
                "$match": {
                    "executed": False,
                }
            },
            {"$sample": {"size": 1}}
        ])

        antigen = ""
        antibody = ""

        for i in element:
            antigen = i["antigen"]
            antibody = i["antibody"]

        antibody_df = df["antibody"][(df["antibody"] == antibody) & (
            df["antigen"] == antigen)].iloc[0]
        antigen_df = df["antigen"][(df["antibody"] == antibody) & (
            df["antigen"] == antigen)].iloc[0]
        antigen_pdb_df = df["antigen_pdb"][(df["antibody"] == antibody) & (
            df["antigen"] == antigen)].iloc[0]
        antigen_chain_df = df["chain"][(df["antibody"] == antibody) & (
            df["antigen"] == antigen)].iloc[0]

        result = first(antibody=antibody_df, antigen=antigen_df, antigen_pdb=antigen_pdb_df,
                       antigen_chain=antigen_chain_df, rosetta_path=rosetta_path)

        if result == False:
            mycol.update_one({
                "antigen": antigen,
                "antibody": antibody
            }, {
                "$set": {
                    "executed": True,
                    "success": False
                }
            })
            continue

        mycol.update_one({
            "antigen": antigen,
            "antibody": antibody
        }, {
            "$set": {
                "executed": True,
                "success": True
            }
        })


if __name__ == "__main__":
    main()

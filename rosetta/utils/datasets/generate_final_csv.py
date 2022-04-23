import os

import pandas as pd

interactions_df = pd.read_csv(os.path.join(
    os.getcwd(), './interactions_filters_post_search.csv'))
resumen_antigen_df = pd.read_csv(os.path.join(
    os.getcwd(), './resume_antigen_info.csv'))

# Borramos las interacciones duplicadas
interactions_df = interactions_df.drop_duplicates(
    subset=["antigen", "antibody"], keep=False)

interactions_df.to_csv(
    "interactions_without_duplicates.csv", index=False, header=True)

interactions_final = pd.merge(
    interactions_df, resumen_antigen_df, on="antigen")

interactions_final = interactions_final[[
    "antibody", "antigen", "pdb_file", "value_intensity", "category_full_space", "filter", "chain"]]

interactions_final.rename(columns={"pdb_file": "antigen_pdb"}, inplace=True)

interactions_final.to_csv(
    "antigen_antibody_interactions.csv", index=False, header=True)

import pandas as pd
import numpy as np

users_data = {"user_id": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "weight": [
    30, 40, 50, 35, 70, 80, 60, 80, 80, 20], "sex": [1, 1, 0, 0, 0, 1, 1, 1, 0, 1]}

movies_data = {"movie_id": [0, 1, 2, 3, 4], "duration": [
    30, 60, 50, 40, 120], "staff": [120, 30, 50, 80, 80]}

users_df = pd.DataFrame(data=users_data)
movies_df = pd.DataFrame(data=movies_data)

relations_df = pd.DataFrame(columns=["user_id", "movie_id", "score"])
for i in range(len(users_df)):
    for j in range(len(movies_data)):
        user = users_df["user_id"].iloc[i]
        movie = movies_df["movie_id"].iloc[j]
        score = np.random.randint(3,size=1)[0]
        new_row = {"user_id": user, "movie_id": movie, "score": score}
        relations_df = relations_df.append(new_row, ignore_index=True)

relations_df["user_id"] = relations_df["user_id"].astype(int)
relations_df["movie_id"] = relations_df["movie_id"].astype(int)

users_df.to_csv("my_datasets/users.csv", index=False, header=True)
movies_df.to_csv("my_datasets/movies.csv", index=False, header=True)
relations_df.to_csv("my_datasets/relations.csv", index=False, header=True)

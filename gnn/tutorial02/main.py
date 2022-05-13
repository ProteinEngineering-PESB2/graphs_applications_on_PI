import pandas as pd
from torch_geometric.data import HeteroData
import torch
from torch_geometric.nn import SAGEConv, to_hetero
import torch_geometric.transforms as T

users_df = pd.read_csv("./my_datasets/users.csv")
movies_df = pd.read_csv("./my_datasets/movies.csv")
relations_df = pd.read_csv("./my_datasets/relations.csv")

users_node_features = users_df[["weight", "sex"]]
movies_node_features = movies_df[["duration", "staff"]]

labels = relations_df["score"]
y = labels.to_numpy()

edge_index = None

def load_edge_csv(path, src_index_col, src_mapping, dst_index_col, dst_mapping,
                  encoders=None, **kwargs):
    df = pd.read_csv(path, **kwargs)

    src = [src_mapping[index] for index in df[src_index_col]]
    dst = [dst_mapping[index] for index in df[dst_index_col]]
    edge_index = torch.tensor([src, dst])

    return edge_index

users_map = relations_df["user_id"].to_dict()
movies_map = relations_df["movie_id"].to_dict()

edge_index = load_edge_csv("./my_datasets/relations.csv", src_index_col="user_id", src_mapping=users_map ,dst_index_col="movie_id", dst_mapping=movies_map)

# edge_index = relations_df[["user_id", "movie_id"]].values.transpose()

data = HeteroData()

data["user"].x = users_node_features.to_numpy()
data["movie"].x = movies_node_features.to_numpy()

data["user", "score", "movie"].edge_index = edge_index

# data["user", "movie"].y = y

data = T.ToUndirected()(data)

class GNN(torch.nn.Module):
    def __init__(self, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

model = GNN(hidden_channels=64, out_channels=3)
model = to_hetero(model, data.metadata(), aggr='sum')
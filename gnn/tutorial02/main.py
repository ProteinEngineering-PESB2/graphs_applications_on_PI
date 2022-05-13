import pandas as pd
from torch_geometric.data import HeteroData
import torch
from torch_geometric.nn import SAGEConv, to_hetero, GATConv
import torch_geometric.transforms as T
import torch.nn.functional as F

users_df = pd.read_csv("./my_datasets/users.csv")
movies_df = pd.read_csv("./my_datasets/movies.csv")
relations_df = pd.read_csv("./my_datasets/relations.csv")

users_node_features = users_df[["weight", "sex"]]
movies_node_features = movies_df[["duration", "staff"]]

users_node_features_tensor = torch.from_numpy(users_node_features.to_numpy()).float()
movies_node_features_tensor = torch.from_numpy(movies_node_features.to_numpy()).float()

labels = relations_df["score"]
y = labels.to_numpy()
y_tensor = torch.from_numpy(y).long()

users_map = relations_df["user_id"].to_dict()
movies_map = relations_df["movie_id"].to_dict()

edge_index = relations_df[["user_id", "movie_id"]].values.transpose()
edge_index_tensor = torch.from_numpy(edge_index).long()

data = HeteroData()

data["user"].x = users_node_features_tensor
data["user"].train_mask = y_tensor
data["user"].y = y_tensor
data["movie"].x = movies_node_features_tensor

data["user", "score", "movie"].edge_index = edge_index_tensor

data["user", "movie"].y = y_tensor

data = T.ToUndirected()(data)

from torch_geometric.nn import GATConv, Linear, to_hetero

class GAT(torch.nn.Module):
    def __init__(self, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GATConv((-1, -1), hidden_channels, add_self_loops=False)
        self.lin1 = Linear(-1, hidden_channels)
        self.conv2 = GATConv((-1, -1), out_channels, add_self_loops=False)
        self.lin2 = Linear(-1, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index) + self.lin1(x)
        x = x.relu()
        x = self.conv2(x, edge_index) + self.lin2(x)
        return x


model = GAT(hidden_channels=64, out_channels=3)
model = to_hetero(model, data.metadata(), aggr='sum')
optimizer = torch.optim.Adam(model.parameters())

print(data)

def train():
    model.train()
    loss = 0
    optimizer.zero_grad()
    out = model(data.x_dict, data.edge_index_dict)
    mask = data['user'].train_mask

    loss = F.cross_entropy(out['user'][mask], data['user'].y[mask])
    loss.backward()
    optimizer.step()
    return float(loss)

result = train()
import pandas as pd
import torch
import torch_geometric.transforms as T
from torch_geometric.data import HeteroData
from torch_geometric.nn import GATConv, to_hetero, Linear, SAGEConv
import torch.nn.functional as F

users_df = pd.read_csv("./my_datasets/users.csv")
movies_df = pd.read_csv("./my_datasets/movies.csv")

users_node_features = users_df[["weight", "sex"]].to_numpy()
users_node_features = torch.from_numpy(users_node_features).float()

movies_node_features = movies_df[["duration", "staff"]].to_numpy()
movies_node_features = torch.from_numpy(movies_node_features).float()

edge_index = users_df[["user_id", "movie_id"]].values.transpose()
edge_index = torch.from_numpy(edge_index).long()

y = users_df["score"].to_numpy()
y = torch.from_numpy(y).long()

data = HeteroData()

data["user"].x = users_node_features
data["user"].y = y
data["movie"].x = movies_node_features

data["user", "score" ,"movie"].edge_index = edge_index

data = T.ToUndirected()(data)
data = T.RandomNodeSplit()(data)

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
optimizer = torch.optim.Adam(model.parameters())

print(data)
print(data.x_dict)
print(data.edge_index_dict)

loss_list = []
for epoch in range(10):
    optimizer.zero_grad()
    out = model(data.x_dict, data.edge_index_dict)
    mask = data["user"].train_mask
    loss = F.nll_loss(out["user"][mask], data["user"].y[mask])
    loss_list.append(loss.item())
    loss.backward()
    optimizer.step()

print(loss_list)
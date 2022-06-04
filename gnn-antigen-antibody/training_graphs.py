import pandas as pd
import numpy as np
import os
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv, global_mean_pool, GraphConv
import torch
from torch.nn import Linear
import torch.nn.functional as F

data_list = []
cont = 0

for file in os.listdir("./carbonos_alfa"):
    print(cont)
    df = pd.read_csv(f"./carbonos_alfa/{file}")

    y = np.array([])
    edge_index = []
    positions = []
    calculates = []

    for i in range(len(df)):
        x_i = df["x"].iloc[i]
        y_i = df["y"].iloc[i]
        z_i = df["z"].iloc[i]

        position_i = df["Unnamed: 0"].iloc[i]

        for j in range(len(df)):
            if i != j:
                x_j = df["x"].iloc[j]
                y_j = df["y"].iloc[j]
                z_j = df["z"].iloc[j]

                point1 = np.array((x_i, y_i, z_i))
                point2 = np.array((x_j, y_j, z_j))

                dist = np.linalg.norm(point1 - point2)

                if ((dist >= 2) and (dist <= 15)):
                    interaction = f"{i}-{j}"
                    reverse_interaction = f"{j}-{i}"

                    if not reverse_interaction in calculates:
                        y = np.append(y, dist)

                        position_j = df["Unnamed: 0"].iloc[j]

                        edge_index.append([position_i, position_j])

                        if not i in positions:
                            positions.append(i)
                        if not j in positions:
                            positions.append(j)
                    
                    calculates.append(interaction)

    df = df.loc[positions]
    df = df.drop(["Unnamed: 0", "residue"], axis=1)

    features = df.values
    x = torch.from_numpy(features).type(torch.float)

    y = y.reshape(1,len(y))
    y = torch.from_numpy(y).float()

    edge_index = np.array(edge_index)
    edge_index = torch.from_numpy(edge_index).type(torch.long)
    edge_index = edge_index.t().contiguous()

    data = Data(x=x, edge_index=edge_index, y=y)

    print(data)

    data_list.append(data)

    cont += 1
    if cont == 1:
        break

train_dataset = data_list[:3]
test_dataset = data_list[2:]

train_loader = DataLoader(train_dataset, shuffle=True)
test_loader = DataLoader(test_dataset, shuffle=False)

class GCN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super(GCN, self).__init__()
        self.hidden_cahnnels = hidden_channels
        self.conv1 = GraphConv(3, hidden_channels)
        self.conv2 = GraphConv(hidden_channels, hidden_channels)
        self.conv3 = GraphConv(hidden_channels, hidden_channels)

    def forward(self, x, edge_index, batch, out_channels):
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        x = x.relu()
        x = self.conv3(x, edge_index)

        x = global_mean_pool(x, batch)

        x = F.dropout(x, p=0.5, training=self.training)

        lin = Linear(self.hidden_cahnnels, out_channels)
        x = lin(x)

        return x

model = GCN(hidden_channels=64)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.CrossEntropyLoss()

def train():
    model.train()

    for data in train_loader:
        out_channels = data.y.shape[1]
        out = model(data.x, data.edge_index, data.batch, out_channels)
        loss = criterion(out, data.y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

def test(loader):
    model.eval()

    correct = 0
    for data in loader:
        out_channels = data.y.shape[1]
        out = model(data.x, data.edge_index, data.batch, out_channels)
        pred = out.argmax(dim=1)
        correct += int((pred == data.y).sum())
    
    return correct / len(loader.dataset)

for epoch in range(1):
    train()
    test_acc = test(test_loader)
    print(test_acc)
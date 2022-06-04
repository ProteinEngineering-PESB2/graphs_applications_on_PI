import os
import pandas as pd
import numpy as np
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
import torch
from torch_geometric.nn import GCNConv, global_mean_pool
from torch.nn import Linear
import torch.nn.functional as F

cont = 0
graph_list = []

for file in os.listdir("./carbonos_alfa"):
    df = pd.read_csv(f"./carbonos_alfa/{file}")

    edge_attr = np.array([])
    edge_index = []
    positions = []

    for i in range(len(df)):
        for j in range(len(df)):
            if i != j:
                x_i = df["x"].iloc[i]
                y_i = df["y"].iloc[i]
                z_i = df["z"].iloc[i]

                x_j = df["x"].iloc[j]
                y_j = df["y"].iloc[j]
                z_j = df["z"].iloc[j]

                point1 = np.array((x_i, y_i, z_i))
                point2 = np.array((x_j, y_j, z_j))

                dist = np.linalg.norm(point1 - point2)

                if ((dist >= 2) and (dist <= 15)):
                    edge_attr = np.append(edge_attr, dist)

                    position_i = df["Unnamed: 0"].iloc[i]
                    position_j = df["Unnamed: 0"].iloc[j]
                    
                    edge_index.append([position_i, position_j])

                    if not i in positions:
                        positions.append(i)
                    if not j in positions:
                        positions.append(j)

    complex_class = np.random.randint(0,3)
    print(complex_class)
    y = [complex_class]
    y = np.array(y)
    y = torch.from_numpy(y).type(torch.long)

    edge_attr = edge_attr.reshape(len(edge_attr), 1)
    edge_attr = torch.from_numpy(edge_attr).type(torch.float)

    edge_index = np.array(edge_index)
    edge_index = torch.from_numpy(edge_index).type(torch.long)
    edge_index = edge_index.t().contiguous()

    df = df[["x","y","z"]].loc[positions]
    x = df.values
    x = torch.from_numpy(x).type(torch.float)

    graph = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y)

    graph_list.append(graph)

    cont += 1
    if cont == 188:
        break

train_dataset = graph_list[:150]
test_dataset = graph_list[150:]

train_loader = DataLoader(train_dataset, shuffle=True)
test_loader = DataLoader(test_dataset, shuffle=False)

class GCN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(3, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.conv3 = GCNConv(hidden_channels, hidden_channels)
        self.lin = Linear(hidden_channels, 3)

    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        x = x.relu()
        x = self.conv3(x, edge_index)

        x = global_mean_pool(x, batch)

        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin(x)

        return x

model = GCN(hidden_channels=64)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.CrossEntropyLoss()

def train():
    model.train()

    for data in train_loader:
        out = model(data.x, data.edge_index, data.batch)
        print(out)
        print(data.y)
        loss = criterion(out, data.y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

def test(loader):
    model.eval()

    correct = 0
    for data in loader:
        out = model(data.x, data.edge_index, data.batch)
        pred = out.argmax(dim=1)
        correct += int((pred == data.y).sum())
    
    return correct / len(loader.dataset)

for epoch in range(1):
    train()
    test_acc = test(test_loader)
    print(test_acc)
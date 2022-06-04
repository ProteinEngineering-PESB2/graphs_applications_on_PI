import networkx as nx
from torch_geometric.utils.convert import from_networkx
from torch_geometric.loader import DataLoader
from torch_geometric.nn import global_mean_pool, GraphConv
import torch
from torch.nn import Linear
import torch.nn.functional as F

G1 = nx.Graph()

G1.add_nodes_from([
    (1, {"y": [1], "x": [0.5, 0.3, 0.3]}),
    (2, {"y": [2], "x": [0.5, 0.3, 0.3]}),
    (3, {"y": [3], "x": [0.5, 0.3, 0.3]}),
    (4, {"y": [2], "x": [0.5, 0.3, 0.3]})
])

G1.add_edges_from([
    (1,2), (2,3), (1,3)
])

G2 = nx.Graph()

G2.add_nodes_from([
    (1, {"y": [1], "x": [0.5, 0.3, 0.3]}),
    (2, {"y": [2], "x": [0.5, 0.3, 0.3]}),
    (3, {"y": [3], "x": [0.5, 0.3, 0.3]}),
    (4, {"y": [2], "x": [0.5, 0.3, 0.3]})
])

G2.add_edges_from([
    (1,2), (2,3), (1,3)
])

graph1 = from_networkx(G1)
graph2 = from_networkx(G2)

print(graph1.y)

data_list = [graph1, graph2]

loader = DataLoader(data_list)

class GCN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super(GCN, self).__init__()
        self.conv1 = GraphConv(3, hidden_channels)
        self.conv2 = GraphConv(hidden_channels, hidden_channels)
        self.conv3 = GraphConv(hidden_channels, hidden_channels)
        self.lin = Linear(hidden_channels, 4)

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

    for data in loader:
        out = model(data.x, data.edge_index, data.batch)
        print(out.shape)
        print(data.y.shape)
        print(out)
        print(data.y)
        loss = criterion(out, data.y)
        # loss.backward()
        # optimizer.step()
        # optimizer.zero_grad()

for epoch in range(1):
    train()
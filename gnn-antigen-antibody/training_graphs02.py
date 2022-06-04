import networkx as nx
from torch_geometric.utils.convert import from_networkx
from torch_geometric.loader import DataLoader
from torch_geometric.nn import global_mean_pool, GraphConv
from torch.nn import Linear
import torch
import torch.nn.functional as F

G1 = nx.read_gpickle("./process_pdbs/1AAX/graph_distance_euclidean_centroid_1AAX.gpickle")
G2 = nx.read_gpickle("./process_pdbs/1AEP/graph_distance_euclidean_alpha_carbon_1AEP.gpickle")
G3 = nx.read_gpickle("./process_pdbs/1DY4/graph_distance_euclidean_alpha_carbon_1DY4.gpickle")

pyg_graph1 = from_networkx(G1)
pyg_graph2 = from_networkx(G2)
pyg_graph3 = from_networkx(G3)

data_list = [pyg_graph1, pyg_graph2, pyg_graph3]

loader = DataLoader(data_list)

class GCN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super(GCN, self).__init__()
        self.conv1 = GraphConv(3, hidden_channels)
        self.conv2 = GraphConv(hidden_channels, hidden_channels)
        self.conv3 = GraphConv(hidden_channels, hidden_channels)
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

    for data in loader:
        out = model(data.x, data.edge_index, data.batch)
        # loss = criterion(out, data.y)
        # loss.backward()
        # optimizer.step()
        # optimizer.zero_grad()

for epoch in range(1):
    train()
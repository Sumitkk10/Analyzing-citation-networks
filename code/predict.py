import networkx as nx
from node2vec import Node2Vec
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import numpy as np
from datetime import datetime
import random

# ---------------- Building the graph -----------------

def load_edges():
    location = "../dataset/Cit-HepPh.txt"
    edges = []
    with open(location, 'r') as f:
        next(f)
        next(f)
        next(f)
        next(f)
        for line in f:
            parts = line.strip().split()
            if(len(parts) > 1):
              edges.append((parts[0], parts[1]))
    return edges

def load_dates():
    G = nx.DiGraph()
    store = {}
    location = "../dataset/cit-HepPh-dates.txt"
    with open(location, 'r') as f:
        next(f)
        for line in f:
            id, date = line.strip().split()
            year = int(date.split('-')[0])
            if(id[0] == '1' and id[1] == '1'): # cross-listed papers
                id = id[2:]
            G.add_node(id, date=date)
            if year not in store:
                store[year] = []
            store[year].append(id)
    return G, store

G, year_nodes = load_dates()
edges = load_edges()
G.add_edges_from(edges)
sorted_years = sorted(year_nodes.keys())
# using 10% of the dataset
num_nodes = int(0.10 * len(G.nodes))
random_nodes = random.sample(G.nodes, num_nodes)
G = G.subgraph(random_nodes)

till = '1997-12-31'
T = datetime.strptime(till, '%Y-%m-%d')

train_nodes = [node for node, attrs in G.nodes(data=True) if 'date' in attrs and datetime.strptime(attrs['date'], '%Y-%m-%d') <= T]
test_nodes = [node for node, attrs in G.nodes(data=True) if 'date' in attrs and datetime.strptime(attrs['date'], '%Y-%m-%d') > T]


G_train = G.subgraph(train_nodes)
G_test = G.subgraph(test_nodes)

node2vec = Node2Vec(G_train, dimensions=64, walk_length=30, num_walks=200, workers=4)
model = node2vec.fit(window=10, min_count=1, batch_words=4)

train_edges = [(u, v) for u, v in G_train.edges() if str(u) in model.wv and str(v) in model.wv]
for i in G_train.nodes():
    for j in G_train.nodes():
        if(i != j and not G_train.has_edge(i, j)):
            train_edges.append((i, j))

test_edges = [(u, v) for u, v in G_test.edges() if str(u) in model.wv and str(v) in model.wv]

X_train = np.array([np.concatenate([model.wv[str(u)], model.wv[str(v)]]) for u, v in train_edges])
y_train = np.ones(len(train_edges))
X_test = np.array([np.concatenate([model.wv[str(u)], model.wv[str(v)]]) for u, v in test_edges])
y_test = np.zeros(len(test_edges))

clf = LogisticRegression()
clf.fit(X_train, y_train)

y_pred = clf.predict_proba(X_test)[:, 1]
roc_auc = roc_auc_score(y_test, y_pred)
print("ROC AUC:", roc_auc)
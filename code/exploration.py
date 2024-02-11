import networkx as nx

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
            edges.append((parts[0], parts[1]))
    return edges

def load_dates():
    G = nx.Graph()
    location = "../dataset/cit-HepPh-dates.txt"
    with open(location, 'r') as f:
        next(f)
        for line in f:
            id, date = line.strip().split()
            G.add_node(id, date=date)
    return G

G = load_dates()
edges = load_edges()
G.add_edges_from(edges)


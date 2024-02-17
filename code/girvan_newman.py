import networkx as nx
import matplotlib.pyplot as plt
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
    G = nx.Graph()
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
# using 1% of the dataset
num_nodes = int(0.01 * len(G.nodes))
random_nodes = random.sample(G.nodes, num_nodes)
G = G.subgraph(random_nodes)

# --------------------- Using Girvan-Newman algorithm for clustering ----------------------------------

def girvan_newman(G, T, sorted_years, year_nodes):
    # t is till which year
    here = []
    for i in sorted_years:
        if(i > T):
            break
        for node in year_nodes[i]:
            if node not in here:
                here.append(node)
    cur_graph = G.subgraph(here)
    comp = nx.community.girvan_newman(cur_graph)
    return comp

T = int(input("Enter the year till which you want the clustering of papers to be done: "))
communities = girvan_newman(G, T, sorted_years, year_nodes)
top_level_communities = next(communities)

node_community = {}
for idx, com in enumerate(top_level_communities):
    for node in com:
        node_community[node] = idx

pos = nx.spring_layout(G)
plt.figure(figsize=(12, 8))
nx.draw(G, pos, node_color=[node_community.get(node, -1) for node in G.nodes()], with_labels=False, cmap=plt.cm.tab20, node_size=10)
plt.show()

# --------------- the number of clusters over time ------------------
here = []
num_of_communities = []
for cur_year in sorted_years:
  for node in year_nodes[cur_year]:
    if node not in here:
      here.append(node)
  cur_graph = G.subgraph(here)
  comp = nx.community.girvan_newman(cur_graph)
  comp = next(comp)
  num_of_communities.append(len(comp))

plt.plot(sorted_years, num_of_communities, marker='o')
plt.xlabel('Year')
plt.ylabel('Number of Communities')
plt.title('Number of Communities in Graph Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ----------------- the size of the largest cluster over time -----------------
here = []
largest_communities = []
for cur_year in sorted_years:
  for node in year_nodes[cur_year]:
    if node not in here:
      here.append(node)
  cur_graph = G.subgraph(here)
  comp = nx.community.girvan_newman(cur_graph)
  comp = next(comp)
  mx = max(len(now) for now in comp)
  largest_communities.append(mx)

plt.plot(sorted_years, largest_communities, marker='o')
plt.xlabel('Year')
plt.ylabel('Size of largest community')
plt.title('Size of the largest community in graph over time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
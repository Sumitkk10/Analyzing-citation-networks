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

# --------------------- Using louvain algorithm for clustering ----------------------------------

def louvain_community_detection(G, t, sorted_years, year_nodes, type):
    # t is till which year
    here = []
    for cur_year in sorted_years:
        if(cur_year > t):
          break
        for node in year_nodes[cur_year]:
            if node not in here:
                here.append(node)
    cur_graph = G.subgraph(here)
    if(type == 2):
      num_nodes = int(0.01 * len(G.nodes))
      random_nodes = random.sample(G.nodes, num_nodes)
      temp_G = G.subgraph(random_nodes)
      comm = nx.community.louvain_communities(temp_G)
      return (comm, temp_G)
    communities = nx.community.louvain_communities(cur_graph)
    # returns a list of tuples [{}, {}]
    return communities
    
T = int(input("Enter the year till which you want the clustering of papers to be done: "))
communities = louvain_community_detection(G, T, sorted_years, year_nodes, 1)
print(communities)

# using 1% of dataset to plot 
comm, temp_G = louvain_community_detection(G, T, sorted_years, year_nodes, 2)
community_dict = {}
for com, nodes in enumerate(comm):
    for node in nodes:
        community_dict[node] = com
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(temp_G)
colors = [community_dict[node] for node in temp_G.nodes()]
nx.draw(temp_G, pos, node_color=colors, with_labels=False, node_size=10)
plt.show()

# --------------- the number of clusters over time ------------------
here = []
num_of_communities = []
for cur_year in sorted_years:
  for node in year_nodes[cur_year]:
    if node not in here:
      here.append(node)
  cur_graph = G.subgraph(here)
  communities = nx.community.louvain_communities(cur_graph)
  num_of_communities.append(len(communities))

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
  communities = nx.community.louvain_communities(cur_graph)
  mx = 0
  for community in communities:
    mx = max(mx, len(community))
  largest_communities.append(mx)

plt.plot(sorted_years, largest_communities, marker='o')
plt.xlabel('Year')
plt.ylabel('Size of largest community')
plt.title('Size of largest community in Graph Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

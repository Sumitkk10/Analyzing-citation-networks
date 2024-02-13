import networkx as nx
import matplotlib.pyplot as plt

# ---------------- Building the graph -----------------

def load_edges():
    location = "/Cit-HepPh.txt"
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
    location = "/cit-HepPh-dates.txt"
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

# ---------------- Using louvain algorithm for clustering -----------------

def louvain_community_detection(G, t, sorted_years, year_nodes):
    # t is till which year
    here = []
    for cur_year in sorted_years:
        if(cur_year > t):
          break
        for node in year_nodes[cur_year]:
            if node not in here:
                here.append(node)
    cur_graph = G.subgraph(here)
    communities = nx.community.louvain_communities(cur_graph)
    # returns a list of tuples [{}, {}]
    return communities
    
T = int(input("Enter the year till which you want the clustering of papers to be done: "))
communities = louvain_community_detection(G, T, sorted_years, year_nodes)
print(communities)

# Lets plot the number of clusters over time
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

# Lets plot the size of the largest cluster over time
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



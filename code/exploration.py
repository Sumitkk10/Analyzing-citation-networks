import networkx as nx
import matplotlib.pyplot as plt

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

# ---------------- Plotting number of papers over time -----------------
papers = []
here = []
for cur_year in sorted_years:
    for node in year_nodes[cur_year]:
        if node not in here:
            here.append(node)
    papers.append(len(here))
plt.plot(sorted_years, papers, marker='o')
plt.xlabel('Year')
plt.ylabel('Number of papers')
plt.title('Number of papers Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------------- Plotting number of citations over time -----------------
citations = []
here = []
for cur_year in sorted_years:
    for node in year_nodes[cur_year]:
        if node not in here:
            here.append(node)
    cur_graph = G.subgraph(here)
    citations.append(len(cur_graph.edges()))
plt.plot(sorted_years, citations, marker='o')
plt.xlabel('Year')
plt.ylabel('Number of Citations')
plt.title('Number of Citations Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------------- Plotting density of the graph -----------------
density = []
here = []
for cur_year in sorted_years:
    for node in year_nodes[cur_year]:
        if node not in here:
            here.append(node)
    cur_graph = G.subgraph(here)
    density.append(nx.density(cur_graph))

plt.plot(sorted_years, density, marker='o')
plt.xlabel('Year')
plt.ylabel('Density')
plt.title('Density of Graph Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------------- Plotting diameter of the graph -----------------
diameters = []
here = []
till = []
for cur_year in sorted_years:
    for node in year_nodes[cur_year]:
        if node not in here:
            here.append(node)
    cur_graph = G.subgraph(here)
    if(cur_year == 1997): # using 50% of the dataset
      break
    till.append(cur_year)
    temp = dict(nx.all_pairs_shortest_path_length(cur_graph))
    mx = max(length for lengths in temp.values() for length in lengths.values())
    diameters.append(mx)

plt.plot(till, diameters, marker='o')
plt.xlabel('Year')
plt.ylabel('Diameter')
plt.title('Diameter of Graph Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------------- Plotting mean degree centrality of the graph -----------------
degrees = []
here = []
for cur_year in sorted_years:
    for node in year_nodes[cur_year]:
        if node not in here:
            here.append(node)
    cur_graph = G.subgraph(here)
    deg_cent = nx.degree_centrality(cur_graph)
    degrees.append(sum(deg_cent.values()) / len(deg_cent))

plt.plot(sorted_years, degrees, marker='o')
plt.xlabel('Year')
plt.ylabel('Mean Degree Centrality')
plt.title('Mean Degree Centrality of Graph Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------------- Plotting avg clustering coefficient of the graph -----------------
coefficient = []
here = []
for cur_year in sorted_years:
    for node in year_nodes[cur_year]:
        if node not in here:
            here.append(node)
    cur_graph = G.subgraph(here)
    coefficient.append(nx.average_clustering(cur_graph))

plt.plot(sorted_years, coefficient, marker='o')
plt.xlabel('Year')
plt.ylabel('Avg clustering coefficient')
plt.title('Avg clustering coefficient of Graph Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------------- Plotting avg closeness centrality of the graph -----------------
closeness = []
here = []
till = []
for cur_year in sorted_years:
    for node in year_nodes[cur_year]:
        if node not in here:
            here.append(node)
    if(cur_year == 2000): # using 75% of the dataset
      break
    till.append(cur_year)
    cur_graph = G.subgraph(here)
    temp = nx.closeness_centrality(cur_graph)
    closeness.append(sum(temp.values()) / len(temp))

plt.plot(till, closeness, marker='o')
plt.xlabel('Year')
plt.ylabel('Avg closeness centrality')
plt.title('Avg closeness centrality of Graph Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
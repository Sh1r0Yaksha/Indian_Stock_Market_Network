import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pyvis.network import Network

colname = 'CH_CLOSING_PRICE'
df = pd.read_csv('correlation_data/correlation_log_diff_' + colname + '.csv')

def plot_threshold(corr_df):
    G = nx.Graph()
    nodes = set(corr_df['FILENAME1'].unique()) | set(corr_df['FILENAME2'].unique())
    G.add_nodes_from(nodes)
    for _, row in corr_df.iterrows():
        weight = row['CORRELATION']
        if row['FILENAME1'] != row['FILENAME2']:
            G.add_edge(row['FILENAME1'], row['FILENAME2'], weight=weight)

    thresholds = np.arange(-1, 1, 0.05)  # Stops before 0.95 to avoid exceeding 0.9
    edge_densities = []

    for thresh in thresholds:
        filtered_edges = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] > thresh]
        edge_density = len(filtered_edges) / (len(nodes) * (len(nodes) - 1) / 2)  # Formula for edge density
        edge_densities.append(edge_density)

    plt.plot(thresholds, edge_densities, marker='o')
    plt.xlabel('Threshold')
    plt.ylabel('Edge Density')
    plt.title('Edge Density vs. Threshold')
    plt.grid(True)
    plt.show()

plot_threshold(df)
threshold = 0.4


def create_network(corr_df, threshold):
    G = nx.Graph()
    nodes = set(corr_df['FILENAME1'].unique()) | set(corr_df['FILENAME2'].unique())
    G.add_nodes_from(nodes)
    for _, row in corr_df.iterrows():
        weight=row['CORRELATION']
        if weight > threshold and row['FILENAME1'] != row['FILENAME2']:
            G.add_edge(row['FILENAME1'], row['FILENAME2'], weight=weight)
    edge_density = (2 * len(G.edges())) / (len(G.nodes()) * (len(G.nodes()) - 1)) # 2E / V(V-1)
    print(f"Edge density of graph at threshold {threshold} is {edge_density}")
    return G

G = create_network(df, threshold)
print(f"Number of edges of network {G.number_of_edges()}")

def sort_and_print_top_x(df, num, centrality):
    sorted_df = sorted(df.items(), key=lambda x: x[1], reverse=True)

    print(f"\nTop 10 central nodes based on {centrality} centrality\n")
    for node, centrality in sorted_df[:num]:
        print(f"Node {node}: {centrality} Centrality = {centrality:.4f}")

def calculate_centrality_measures(network):

    # Calculate the degree centrality
    degree_centrality = nx.degree_centrality(network)
    sort_and_print_top_x(degree_centrality, 10, 'degree')

    # Calculate the betweenness centrality
    betweenness_centrality = nx.betweenness_centrality(network)
    sort_and_print_top_x(betweenness_centrality, 10, 'betweenness')

    pagerank = nx.pagerank(network, max_iter=2000)
    sort_and_print_top_x(pagerank, 10, 'pagerank')

    eigenvector_centrality = nx.eigenvector_centrality(network)
    sort_and_print_top_x(eigenvector_centrality, 10, 'eigenvector')

calculate_centrality_measures(G)

net = Network()
net.from_nx(G)

# net.toggle_physics(False)
# net.show_buttons(filter_=['physics'])

net.force_atlas_2based(
    # theta = 0.5,
    gravity=-50, 
    central_gravity=0.01, 
    spring_length=100,
    spring_strength=0.08, 
    damping=0.4, 
    overlap=0
)


net.save_graph('out.html')

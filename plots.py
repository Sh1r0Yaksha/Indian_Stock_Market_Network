import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def plot_threshold(colname):
    corr_df = pd.read_csv('correlation_data/correlation_log_diff_' + colname + '.csv')
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

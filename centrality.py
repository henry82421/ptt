import csv
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


csvname = 'c://x.csv'

coocc = pd.DataFrame.from_csv(csvname)
adjacency = coocc.as_matrix(columns=None)
print adjacency

def get_labels(csvfile):
    with open(csvfile) as f:
        reader = csv.reader(f)
        # get the first line in csv
        labels = reader.next()
    # return just the letters from pos 1 on
    return labels[1:]


def make_label_dict(labels):
    l = {}
    for i, label in enumerate(labels):
        l[i] = label
    return l
label_dict = make_label_dict(get_labels('c://x.csv'))
print label_dict    
 


def calculate_graph(adjacency_matrix, mylabels):
#     here is the syntax for some other graphing options
#     ,graph_layout='shell',
#                node_size=1600, node_color='blue', node_alpha=0.3,
#                node_text_size=12,
#                edge_color='blue', edge_alpha=0.3, edge_tickness=1,
#                edge_text_pos=0.3,
#                text_font='sans-serif'):
    rows, cols = np.where(adjacency_matrix != 0)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    avg_connect_dist = []
    count = 0
    for node in gr.nodes_iter():
        length=nx.single_source_dijkstra_path_length(gr,node)
        avg_connect_dist.append(np.mean(length.values()))
    actor_name = mylabels.values()
    return avg_connect_dist, actor_name, gr

avg_connect_dist, actor_name, gr = calculate_graph(adjacency, make_label_dict(get_labels(csvname)))
# This just checks for node numbers of specific actors in case you want 
# to calculate something like the Bacon Number
def actor_node(name,actor_name):
    for i, j in enumerate(actor_name):
        if j == name:       
            print i, j

# a pandas dataframe of actors and their average connectivity for your viewing pleasure
actor_connect_dist = [actor_name,avg_connect_dist]
actor_connect_dist = zip(*actor_connect_dist)
columns = ['ActorName','AvgConnectivity']
ActorConnectDF = pd.DataFrame(actor_connect_dist,columns = columns)
print ActorConnectDF


betweenness = nx.closeness_centrality(gr)
between = betweenness.items()
between.sort(key=lambda x:x[1],reverse=True)
print between

nx.draw_circular(gr,labels=label_dict, with_labels=True)
plt.show()     

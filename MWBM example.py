#           Last Update April 5th 2019      #
#                                          #
#                                         #
#                                        #
#       Just a simple bipartite graph   #
#       MWBM Example                   #
#######################################




import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


##Get the x and y positions (for the node) for plotting
def get_bipartite_positions(graph):
    pos = {}
    u = 0
    v = 0
    for i, n in enumerate(graph.nodes()):
        x = 0 if 'u' in n else 1 #u:0, v:1
        if(x==0):
            u += 1
            pos[n] = (x,u)
        else:
            v += 1
            pos[n] = (x,v)
    return pos


G = nx.Graph()
#nodes
G.add_node('u3')
G.add_node('u2')
G.add_node('u1')
G.add_node('v4')
G.add_node('v3')
G.add_node('v2')
G.add_node('v1')
#edges
G.add_edge('u3', 'v4', weight=0.2)
G.add_edge('u2', 'v4', weight=0.1)
G.add_edge('u3', 'v2', weight=0.7)
G.add_edge('u2', 'v1', weight=0.4)
G.add_edge('u1', 'v1', weight=0.5)
G.add_edge('u1', 'v3', weight=0.3)


edges = [(u, v) for (u, v, d) in G.edges(data=True)]
pos = get_bipartite_positions(G)  # positions for all nodes
match= nx.max_weight_matching(G)
matchlist = list(match)
# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)
# edges
nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, alpha=0.5, edge_color='b', style='dashed')
nx.draw_networkx_edges(G, pos, edgelist=matchlist, width=6)
# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
plt.axis('off')
plt.show()

#           Last Update April 5th 2019      #
#                                          #
#                                         #
#                                        #
#       various functions to help with  #
#       MWBM and plotting the graph    #
#       *Probably not going to use    #
#######################################

import math
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

##create a bipartite graph given U,V(lists) and E -- E's type might change (depending on how we implement it)
def graph(U,V,E,n):
	G = nx.Graph()
	for u in U:
		G.add_node(u)
		for v in V:
			G.add_node(v)
			G.add_edge(u, v, weight=E[u][v][n]) 
	return G

##Plot before MWBM
def plotGraph(G):
	edges = [(u, v) for (u, v, d) in G.edges(data=True)]
	pos = get_bipartite_positions(G)  # positions for all nodes
	# nodes
	nx.draw_networkx_nodes(G, pos, node_size=700)
	# edges
	nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, alpha=0.5, edge_color='b', style='dashed')
	# labels
	nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
	plt.axis('off')
	plt.show()

##Plot After MWBM
def plotGraph(G,match):
	edges = [(u, v) for (u, v, d) in G.edges(data=True)]
	matchlist = list(match)
	pos = get_bipartite_positions(G)  # positions for all nodes
	# nodes
	nx.draw_networkx_nodes(G, pos, node_size=700)
	# edges
	nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, alpha=0.5, edge_color='b', style='dashed')
	nx.draw_networkx_edges(G, pos, edgelist=matchlist, width=6)
	# labels
	nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
	plt.axis('off')
	plt.show()

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

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G=nx.DiGraph()

G.add_node(1)

G.add_node(2)
G.add_edge(1,2)
nx.draw(G)
plt.show()
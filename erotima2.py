import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx

# G = nx.Graph()
# G.add_nodes_from(range(100), bipartite=0)
# G.add_nodes_from(range(100), bipartite=1)
#
# costs = [
#     [1,2,3,4,5],
#     [1,2,3,4,5],
#     [32,34,5,66,77],
#     [32,34,5,66,77],
#     [32,34,5,66,77],
# ]
#
# for i in range(len(costs)):
#     for j in range(len(costs[i])):
#         G.add_edges_from([(i, j, {'weight': costs[i][j]})])



from helpers import extract_data
mitsos = extract_data(output_type="graph")
print(mitsos)
print(mitsos[1])

matching = nx.bipartite.minimum_weight_full_matching(mitsos[1], weight='weight')
print(matching)
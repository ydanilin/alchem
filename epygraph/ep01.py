# -*- coding: utf-8 -*-
import gvzpassage


handle = gvzpassage.agraphNew('DjHuj', directed=True)
node1 = gvzpassage.addNode(handle, "HUJ_1")
node2 = gvzpassage.addNode(handle, "HUJ_2")
node3 = gvzpassage.addNode(handle, "HUJ_3")
node4 = gvzpassage.addNode(handle, "HUJ_4")
edge1 = gvzpassage.addEdge(handle, node1, node2, "rebro12")
edge2 = gvzpassage.addEdge(handle, node1, node3)
edge3 = gvzpassage.addEdge(handle, node3, node4)
dic = gvzpassage.layout(handle)
print('Graph before delete node HUJ_4:')
gvzpassage.stdout_graph(handle)
# print('')
gvzpassage.delete_edge(handle, edge3)
gvzpassage.delete_node(handle, node4)
print('Graph AFTER delete node HUJ_4:')
gvzpassage.stdout_graph(handle)

ng = gvzpassage.node_geometry(node3)
eg = gvzpassage.edge_geometry(edge2)

# print(dic)
# print(ng)
print(eg)

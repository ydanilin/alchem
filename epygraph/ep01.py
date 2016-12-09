# -*- coding: utf-8 -*-
import gvzpassage


handle = gvzpassage.agraphNew('DjHuj', directed=True)
node1 = gvzpassage.addNode(handle, "HUJ_1")
node2 = gvzpassage.addNode(handle, "HUJ_2")
node3 = gvzpassage.addNode(handle, "HUJ_3")
edge1 = gvzpassage.addEdge(handle, node1, node2, "rebro12")
edge2 = gvzpassage.addEdge(handle, node1, node3)
dic = gvzpassage.layout(handle)

print(dic)

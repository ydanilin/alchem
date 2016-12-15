# -*- coding: utf-8 -*-
import gvzpassage


class AGraph:
    def __init__(self, directed=True):
        self.graphPtr = gvzpassage.agraphNew('DjHuj', directed)
        self.nodesPtr = []
        self.nodesPtr.append(gvzpassage.addNode(self.graphPtr, "1"))
        self.nodesPtr.append(gvzpassage.addNode(self.graphPtr, "2"))
        self.nodesPtr.append(gvzpassage.addNode(self.graphPtr, "3"))
        self.nodesPtr.append(gvzpassage.addNode(self.graphPtr, "4"))
        self.edge1Ptr = gvzpassage.addEdge(self.graphPtr, self.nodesPtr[0], self.nodesPtr[1])
        self.edge2Ptr = gvzpassage.addEdge(self.graphPtr, self.nodesPtr[0], self.nodesPtr[2])
        self.edge3Ptr = gvzpassage.addEdge(self.graphPtr, self.nodesPtr[2], self.nodesPtr[3])
        self.boundingBox = gvzpassage.layout(self.graphPtr)
        # print('Graph before delete node HUJ_4:')
        # gvzpassage.stdout_graph(self.graphPtr)
        # gvzpassage.delete_edge(self.graphPtr, edge3)
        # gvzpassage.delete_node(self.graphPtr, node4)
        # print('Graph AFTER delete node HUJ_4:')
        # gvzpassage.stdout_graph(self.graphPtr)

        self.nodesGeom = []
        for nodePtr in self.nodesPtr:
            self.nodesGeom.append(gvzpassage.node_geometry(nodePtr))
        # eg = gvzpassage.edge_geometry(edge2)

if __name__ == '__main__':
    a = AGraph()

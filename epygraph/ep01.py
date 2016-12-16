# -*- coding: utf-8 -*-
import epygraph.gvzpassage as gps


class AGraph:
    def __init__(self, directed=True):
        self.graphPtr = gps.agraphNew('DjHuj', directed)
        gps.set_shape_nodes(self.graphPtr, 'circle')
        self.nodesPtr = []
        self.nodesPtr.append(gps.addNode(self.graphPtr, "1"))
        self.nodesPtr.append(gps.addNode(self.graphPtr, "2"))
        self.nodesPtr.append(gps.addNode(self.graphPtr, "3"))
        self.nodesPtr.append(gps.addNode(self.graphPtr, "4"))
        self.edge1Ptr = gps.addEdge(self.graphPtr, self.nodesPtr[0], self.nodesPtr[1])
        self.edge2Ptr = gps.addEdge(self.graphPtr, self.nodesPtr[0], self.nodesPtr[2])
        self.edge3Ptr = gps.addEdge(self.graphPtr, self.nodesPtr[2], self.nodesPtr[3])
        self.boundingBox = gps.layout(self.graphPtr)
        # print('Graph before delete node HUJ_4:')
        # gps.stdout_graph(self.graphPtr)
        # gps.delete_edge(self.graphPtr, edge3)
        # gps.delete_node(self.graphPtr, node4)
        # print('Graph AFTER delete node HUJ_4:')
        # gps.stdout_graph(self.graphPtr)

        self.nodesGeom = []
        for nodePtr in self.nodesPtr:
            self.nodesGeom.append(gps.node_geometry(nodePtr))
        # eg = gvzpassage.edge_geometry(edge2)

if __name__ == '__main__':
    a = AGraph()
    print(a.nodesGeom)

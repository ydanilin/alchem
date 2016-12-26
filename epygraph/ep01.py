# -*- coding: utf-8 -*-
import pprint
import epygraph.gvzpassage as gps


class AGraph:
    def __init__(self, directed=True):
        self.graphPtr, self.graphContext = gps.agraphNew('DjHuj', directed)
        gps.set_shape_nodes(self.graphPtr, 'circle')
        self.nodesPtr = []
        self.nodesPtr.append(gps.addNode(self.graphPtr, "1"))  # 0
        self.nodesPtr.append(gps.addNode(self.graphPtr, "6"))  # 1
        self.nodesPtr.append(gps.addNode(self.graphPtr, "2"))  # 2
        self.nodesPtr.append(gps.addNode(self.graphPtr, "3"))  # 3
        self.nodesPtr.append(gps.addNode(self.graphPtr, "4"))  # 4
        self.nodesPtr.append(gps.addNode(self.graphPtr, "5"))  # 5
        self.edge1Ptr = gps.addEdge(self.graphPtr, self.nodesPtr[0], self.nodesPtr[1])
        self.edge2Ptr = gps.addEdge(self.graphPtr, self.nodesPtr[0], self.nodesPtr[2])
        self.edge3Ptr = gps.addEdge(self.graphPtr, self.nodesPtr[0], self.nodesPtr[3])
        self.edge4Ptr = gps.addEdge(self.graphPtr, self.nodesPtr[3], self.nodesPtr[4])
        self.edge5Ptr = gps.addEdge(self.graphPtr, self.nodesPtr[3], self.nodesPtr[5])
        self.boundingBox = gps.layout(self.graphPtr, self.graphContext)
        # print('Graph before delete node HUJ_4:')
        # gps.stdout_graph(self.graphPtr)
        # gps.delete_edge(self.graphPtr, edge3)
        # gps.delete_node(self.graphPtr, node4)
        # print('Graph AFTER delete node HUJ_4:')
        # gps.stdout_graph(self.graphPtr)

        self.nodesGeom = []
        self.edgesGeom = []
        for nodePtr in self.nodesPtr:
            self.nodesGeom.append(gps.node_geometry(nodePtr))
        self.edgesGeom.append(gps.edge_geometry(self.edge1Ptr))
        self.edgesGeom.append(gps.edge_geometry(self.edge2Ptr))
        self.edgesGeom.append(gps.edge_geometry(self.edge3Ptr))
        self.edgesGeom.append(gps.edge_geometry(self.edge4Ptr))
        self.edgesGeom.append(gps.edge_geometry(self.edge5Ptr))
        # eg = gvzpassage.edge_geometry(edge2)

    def nodeLabel(self, nodePtr):
        return gps.node_label(nodePtr)

    def nodeGeometry(self, nodePtr):
        return gps.node_geometry(nodePtr)

    def closeGraph(self):
        if self.graphPtr:
            gps.agraphClose(self.graphPtr)

if __name__ == '__main__':
    a = AGraph()
    print(a.nodesGeom)
    pp = pprint.PrettyPrinter()
    # pp.pprint(a.edgesGeom)
    print(gps.node_label(a.nodesPtr[-1]))
    a.closeGraph()

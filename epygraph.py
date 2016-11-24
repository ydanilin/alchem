from __future__ import print_function
from __future__ import division

import warnings
import pygraphviz as pgv
from dbms import *


# ignore Graphviz warning messages
# warnings.simplefilter('ignore', RuntimeWarning)


class Epygraph:
    def __init__(self):
        self.dbms = DBMS()
        tree = self.dbms.listAll()

        self.agraph = pgv.AGraph()
        self.agraph.graph_attr['directed'] = True
        self.agraph.node_attr['shape']='circle'

        for node in tree:
            self.agraph.add_node(node['node'])
            if node['path']:
                self.agraph.add_edge(node['parent'], node['node'])

        self.gdata = {}

    def redraw(self):
        self.agraph.layout(prog='dot')
        # you cannot get 'bb' attribute normal way, because it is a BUG.
        # thanks to Aric (https://groups.google.com/forum/#!topic/pygraphviz-discuss/QYXumyw3E-g)
        # for providing the trick "pgv.graphviz.agget(self.agraph.handle, 'bb')"
        self.gdata['bbox'] = pgv.graphviz.agget(self.agraph.handle, 'bb')
        self.gdata['nodes'] = self.agraph.nodes()
        self.gdata['edges'] = self.agraph.edges()
        return self.gdata


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
        self.agraph = pgv.AGraph()
        self.agraph.graph_attr['directed'] = True
        self.gdata = {}

    def redraw(self):
        # self.agraph.clear()
        tree = self.dbms.listAll()
        for node in tree:
            self.agraph.add_node(node['node'])
            if node['path']:
                self.agraph.add_edge(node['parent'], node['node'])
        self.agraph.layout(prog='dot')
        self.gdata['gattrs'] = self.agraph.graph_attr
        self.gdata['nodes'] = self.agraph.nodes()
        self.gdata['edges'] = self.agraph.edges()
        return self.gdata

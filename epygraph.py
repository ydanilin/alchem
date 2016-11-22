import warnings
import pygraphviz as pgv
from dbms import *


# ignore Graphviz warning messages
warnings.simplefilter('ignore', RuntimeWarning)


class Epygraph:
    def __init__(self):
        self.dbms = DBMS()
        self.agraph = pgv.AGraph(name='trial', directed=True)

    def redraw(self):
        self.agraph.clear()
        tree = self.dbms.listAll()
        for node in tree:
            self.agraph.add_node(node['node'])
            if node['path']:
                self.agraph.add_edge(node['parent'], node['node'])
        self.agraph.layout(prog='dot')
        puk = 1
        # TODO: output dictionary with graph geometry

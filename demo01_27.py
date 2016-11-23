#!/usr/bin/env python
from __future__ import print_function
from __future__ import division

def my_graph():
    G = pgv.AGraph(name='miles_dat', directed=True)
    # G.graph_attr['ratio'] = 'fill' # fits both sides of scene rectangle
    G.graph_attr['ratio'] = 'expand' # fits largest side
    G.graph_attr['size'] = '4,4!' # in inches
    G.node_attr['shape']='circle'
    # G.node_attr['fixedsize']='true'
    # G.node_attr['fontsize']='8'
    # G.node_attr['style']='filled'
    # G.graph_attr['outputorder']='edgesfirst'
    # G.graph_attr['label']="miles_dat"
    # G.graph_attr['ratio']='1.0'
    # G.edge_attr['color']='#1100FF'
    # G.edge_attr['style']='setlinewidth(2)'
    
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_node(5)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(2, 5)
    
    return G

if __name__ == '__main__':
    import warnings
    import pygraphviz as pgv

    # ignore Graphviz warning messages
    warnings.simplefilter('ignore', RuntimeWarning)

    G = my_graph()
    G.layout(prog='dot')
    # dim = G.graph_attr['bb'].split(',')

    print('Graph attributes:')
    for k, v in G.graph_attr.items():
        print('{:10}: {:^10}'.format(k, v))

    # print('\nGraph bounding box:')
    # placeholder = '{:<20}{:^12}{:^12}'
    # print(placeholder.format('Bottom left (x, y):', dim[0], dim[1]))
    # print(placeholder.format('Top right (x, y):', dim[2], dim[3]))

    print('\nNode geometry (coordinates from left bottom):')
    placeholder1 = '{:^8}{:^10}{:^10}{:^12}{:^12}'
    print(placeholder1.format('name', 'width', 'height', 'x', 'y'))
    for node in G.nodes():
        name = node.name
        width = node.attr['width']
        height = node.attr['height']
        x, y = node.attr['pos'].split(',')
        print(placeholder1.format(name, width, height, x, y))
    print('\nEdge layout:')
    placeholder2 = '{:^11}'
    print(placeholder2.format('from - to'))
    for edge in G.edges():
        from_to = '{0} - {1}'.format(edge[0], edge[1])

        pos = edge.attr['pos'].split(' ')
        pos_repr = ''
        for elem in pos:
            parts = elem.split(',')
            prefix = ''
            i = 0
            j = 1
            if len(parts) == 3:
                prefix = parts[0]
                i = 1
                j = 2
            x = parts[i]
            y = parts[j]
            pos_repr += prefix + ' ' + x + '  ' + y + '    '

        print(placeholder2.format(from_to), pos_repr)
    G.draw("my.png")
    print("\nCompleted")


# coding=utf-8
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer,
                        UniqueConstraint, select, union, or_, and_, update,
                        literal_column, column)


class DBMS:
    def __init__(self):
        self.engine = create_engine('sqlite:///ierarch01.db')
        self.connection = self.engine.connect()
        self.metadata = MetaData()

        self.t_data = Table('t_data', self.metadata,
                            Column('node', Integer(), primary_key=True),
                            Column('parent', Integer(), nullable=False)
                            )
        self.t_path = Table('t_path', self.metadata,
                            Column('node', Integer()),
                            Column('ancestor', Integer()),
                            UniqueConstraint('node', 'ancestor',
                                             name='path_entry')
                            )
        self.metadata.create_all(self.engine)

        self.data_ins = self.t_data.insert(prefixes=['OR IGNORE'])
        self.data_list = [
            {'node': 1, 'parent': 1},
            {'node': 2, 'parent': 1},
            {'node': 3, 'parent': 1},
            {'node': 4, 'parent': 2},
            {'node': 5, 'parent': 2},
            {'node': 6, 'parent': 5}
        ]
        self.path_ins = self.t_path.insert().prefix_with('OR IGNORE')
        self.path_list = [
            {'node': 2, 'ancestor': 1},
            {'node': 3, 'ancestor': 1},
            {'node': 4, 'ancestor': 2},
            {'node': 4, 'ancestor': 1},
            {'node': 5, 'ancestor': 2},
            {'node': 5, 'ancestor': 1},
            {'node': 6, 'ancestor': 5},
            {'node': 6, 'ancestor': 2},
            {'node': 6, 'ancestor': 1}
        ]
        self.connection.execute(self.data_ins, self.data_list)
        self.connection.execute(self.path_ins, self.path_list)

    def addNode(self, id_, parent, child=None):
        addToData = self.t_data.insert().values((id_, parent))
        subset = select([id_, parent]).union(
                 select([id_, self.t_path.c.ancestor]).where(
                                                  self.t_path.c.node == parent))
        addToPath = self.t_path.insert().from_select(
            ['node', 'ancestor'], subset)
        self.connection.execute(addToData)
        self.connection.execute(addToPath)

    def deleteNode(self, id_, child=None):
        delFromData = self.t_data.delete().where('node' == id_)
        self.connection.execute(delFromData)

    def moveNode(self, id_, moveTo):
        # update t_data
        upd = update(self.t_data).where(self.t_data.c.node == 5).values(
            parent=3)
        self.connection.execute(upd)

        # update t_path
        subtree = select([self.t_path.c.node]).where(self.t_path.c.ancestor == 5)
        path = select([self.t_path.c.ancestor]).where(self.t_path.c.node == 5)

        # deletion
        cond = and_(or_(self.t_path.c.node == 5,
                        self.t_path.c.node.in_(subtree)),
                    self.t_path.c.ancestor.in_(path)
                    )
        delet = self.t_path.delete().where(cond)
        self.connection.execute(delet)

        # insertion
        subtree = select([self.t_path.c.node]).where(self.t_path.c.ancestor == 5)
        path = select([self.t_path.c.ancestor]).where(self.t_path.c.node == 5)
        path_y = select([self.t_path.c.ancestor]).where(self.t_path.c.node == 3)
        subset = select([column('node'), column('ancestor')]).select_from(union(select([literal_column('1').label('sortir'),
                               literal_column('5').label('node'),
                               literal_column('3').label('ancestor')]),
                       select([2, 5, path_y]),
                       select([3, subtree, 3]),
                       select([4, subtree, path_y])).order_by('sortir')
                                      )
        addToPath = self.t_path.insert().from_select(
            ['node', 'ancestor'], subset)
        self.connection.execute(addToPath)

    def listAll(self):
        """output: [{'node': id, 'parent': id, 'path': [id, id, ...]}, ...]"""
        res = self.connection.execute(select([self.t_data.c.node, self.t_data.c.parent]))
        nodes = [dict(n) for n in res]
        for node in nodes:
            sql_path = select([self.t_path.c.ancestor]).where(self.t_path.c.node == node['node'])
            path = [n[0] for n in self.connection.execute(sql_path)]
            node['path'] = path
        return nodes

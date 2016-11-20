# coding=utf-8
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer,
                        UniqueConstraint, select, union, or_, and_, update)


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
        pass

    def debugg(self):
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
        path_y = select([self.t_path.c.ancestor]).where(self.t_path.c.node == 3)
        subset = union(select([5, 3]),
                       select([5, path_y]),
                       select([subtree, 3]),
                       select([subtree, path_y]))
        # subset = union(select([5, 3]),
        #                select([5, self.t_path.c.ancestor]).where(self.t_path.c.node == 3),
        #                select([self.t_path.c.node, 3]).where(self.t_path.c.ancestor == 5),
        #                select([subtree, path_y]))
        res = self.connection.execute(subset)
        for e in res:
            print(e)
        addToPath = self.t_path.insert().from_select(
            ['node', 'ancestor'], subset)
        print(str(subset))
        self.connection.execute(addToPath)

if __name__ == '__main__':
    D = DBMS()
    # D.addNode(9, 6)
    # D.debugg()

# res = [dict(r) for r in rp]
# res = [r for r in rp]

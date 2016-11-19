# coding=utf-8
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer,
                        UniqueConstraint, select)

engine = create_engine('sqlite:///ierarch01.db')
connection = engine.connect()
metadata = MetaData()

t_data = Table('t_data', metadata,
               Column('node', Integer(), primary_key=True),
               Column('parent', Integer(), nullable=False)
               )
t_path = Table('t_path', metadata,
               Column('node', Integer()),
               Column('ancestor', Integer()),
               UniqueConstraint('node', 'ancestor', name='path_entry')
               )

metadata.create_all(engine)

data_list = [
    {'node': 1, 'parent': 1},
    {'node': 2, 'parent': 1},
    {'node': 3, 'parent': 1},
    {'node': 4, 'parent': 2},
    {'node': 5, 'parent': 2},
    {'node': 6, 'parent': 5}
]
path_list = [
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

data_ins = t_data.insert(prefixes=['OR IGNORE'])
path_ins = t_path.insert().prefix_with('OR IGNORE')
print(str(data_ins))

res_d = connection.execute(data_ins, data_list)
res_p = connection.execute(path_ins, path_list)

X = 5
s = select([X, t_path.c.ancestor]).where(t_path.c.node == X)
rp = connection.execute(s)


# res = [dict(r) for r in rp]
# res = [r for r in rp]

print(str(s))
# print(res)
# print(rp)
for ryad in rp:
    print(ryad)

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

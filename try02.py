# coding=utf-8
from sqlalchemy import (create_engine, MetaData, Table, Column, ForeignKey,
                        Integer, Numeric, String, Boolean, DateTime)
from sqlalchemy.sql import select


engine = create_engine('sqlite:///cookies.db')
connection = engine.connect()
metadata = MetaData(engine)

puk = 1
# s = select([cookies])


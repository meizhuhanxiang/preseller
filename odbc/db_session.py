#!/usr/bin/python
# encoding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
__author__ = 'guoguangchuan'

DB_CONNECT_STRING = 'mysql+mysqldb://root:123@localhost/ooxx?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import TypeDecorator
from sqlalchemy import types
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import BOOLEAN
from sqlalchemy import text
from sqlalchemy import DateTime
from model.base import *

__author__ = 'guoguangchuan'


class DetailModel(Base):
    __tablename__ = 'detail'

    id = Column(Integer, primary_key=True)
    fk_id = Column(Integer, nullable=False)
    fk_type = Column(Integer, nullable=False)
    title = Column(String(40), nullable=False, doc="title")
    text = Column(String(300), nullable=False, doc="text")
    image = Column(String(30), nullable=False, doc="image")
    is_del = Column(BOOLEAN, nullable=False, server_default='0', doc="逻辑删除, true(删除1)|false(未删除0)")
    update_time = Column(TIMESTAMP, nullable=False)
    create_time = Column(TIMESTAMP, nullable=False)
    FK_TYPE_PUBLISHER = 0
    FK_TYPE_RULE = 1

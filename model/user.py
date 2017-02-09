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


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(30), nullable=False, server_default=text("''"))
    open_id = Column(String(30), nullable=False, server_default=text("''"))
    sex = Column(String(6), nullable=False, server_default=text("''"))
    province = Column(String(20), nullable=False, server_default=text("''"))
    city = Column(String(20), nullable=False, server_default=text("''"))
    country = Column(String(20), nullable=False, server_default=text("''"))
    profile = Column(String(150), nullable=False, server_default=text("''"))
    privilege = Column(List, nullable=False, server_default=text("''"))
    union_id = Column(String(30), nullable=False, server_default=text("''"))
    is_v = Column(Integer, nullable=False, server_default=text("'0'"))
    name = Column(String(16), nullable=True)
    job = Column(String(30), nullable=True)
    company = Column(String(30), nullable=True)
    phone = Column(Integer, nullable=True)
    email = Column(String(30), nullable=True)
    is_del = Column(BOOLEAN, nullable=False, server_default='0', doc="逻辑删除, true(删除)|false(未删除)")
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_time = Column(TIMESTAMP, nullable=False, server_onupdate=text("CURRENT_TIMESTAMP"))

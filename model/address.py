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
from sqlalchemy import Float
from sqlalchemy import Float
from model.base import *

__author__ = 'guoguangchuan'


class AddressModel(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String(20), nullable=True)
    country = Column(String(20), nullable=False, default="中国")
    province = Column(String(20), nullable=False)
    reginon = Column(String(20), nullable=False)
    address = Column(String(60), nullable=False)
    phone = Column(Integer, nullable=False)
    default = Column(BOOLEAN, nullable=False, server_default='0')
    is_del = Column(BOOLEAN, nullable=False, server_default='0', doc="逻辑删除, true(删除)|false(未删除)")
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_time = Column(TIMESTAMP, nullable=False, server_onupdate=text("CURRENT_TIMESTAMP"))

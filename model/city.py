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


class CityModel(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=True)
    parent_id = Column(Integer, nullable=False, default="中国")
    first_letter = Column(String(10), nullable=False)
    level = Column(Integer, nullable=False)
    is_del = Column(BOOLEAN, server_default="0", nullable=False)

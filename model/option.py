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


class OptionModel(Base):
    __tablename__ = 'option'

    id = Column(Integer, primary_key=True)
    commodity_id = Column(Integer, nullable=False, doc="商品id")
    attr_id = Column(Integer, nullable=False, doc="属性id")
    option_name = Column(String(20), nullable=False, doc="具体分类名字")
    cn_option_name = Column(String(20), nullable=False, doc="中文具体分类名字")
    default = Column(BOOLEAN, nullable=False, server_default='0', doc="是否是已选项")
    weight = Column(Integer, nullable=False, server_default='0', doc="每种类型的价格权重")
    desc = Column(String(30), nullable=True, doc="属性描述")
    index = Column(Integer, nullable=False, doc="排列顺序")
    is_del = Column(BOOLEAN, nullable=False, server_default='0', doc="逻辑删除, true(删除)|false(未删除)")
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    create_time = Column(TIMESTAMP, nullable=False)

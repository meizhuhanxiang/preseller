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


class PublisherModel(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    name = Column(String(30), nullable=False, doc="发布方")
    brief_introduction = Column(String(60), nullable=False, doc="发布方简介")
    admin_name = Column(String(16), nullable=False, doc="负责人姓名")
    admin_phone = Column(Integer, nullable=False, doc="负责人手机号")
    admin_id_card_number = Column(String(20), nullable=False, doc="负责人身份证号")
    tag_title = Column(String(20), nullable=False, doc="标签标题")
    tag_content = Column(String(60), nullable=False, doc="标签内容")
    is_del = Column(BOOLEAN, nullable=False, server_default='0', doc="逻辑删除, true(删除)|false(未删除)")
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_time = Column(TIMESTAMP, nullable=False, server_onupdate=text("CURRENT_TIMESTAMP"))

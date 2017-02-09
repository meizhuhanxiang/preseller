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
from model.base import *

__author__ = 'guoguangchuan'


class CommodityModel(Base):
    __tablename__ = 'commodity'

    id = Column(Integer, primary_key=True)
    title = Column(String(40), nullable=False)
    brief = Column(String(100), nullable=False)
    presell_count = Column(Integer, nullable=False, doc="总共想预售的数量")
    sold_count = Column(Integer, nullable=False, doc="已经卖的数量")
    satisfy_count = Column(Integer, nullable=False, doc="满多少件发货")
    publisher_id = Column(Integer, nullable=False, doc="发布方id")
    base_price = Column(Float(recision=2), doc="基础价格")
    is_del = Column(BOOLEAN, nullable=False, server_default='0', doc="逻辑删除, true(删除1)|false(未删除0)")
    detail_img_count = Column(Integer, nullable=False, doc="商品详情图片总数量")
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_time = Column(TIMESTAMP, nullable=False, server_onupdate=text("CURRENT_TIMESTAMP"))

    def recommend(self, purchase_id):
        sql = 'select u.profile, u.name, u.job, u.is_v, r.content from `recommend` r ' \
              'left join `user` u on r.user_id=u.id where r.purchase_id=%s'
        res = self.fetch_all(sql, [purchase_id], 'dict')
        return res

    def publisher(self, purchase_id):
        sql = 'select p.brief_introduction, p.tag_title, p.tag_content'

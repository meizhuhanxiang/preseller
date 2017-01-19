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


class OrderModel(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, doc="用户id")
    commodity_id = Column(Integer, nullable=False, doc="商品id")
    selected_option_ids = Column(List, nullable=False, doc="选中的属性id")
    count = Column(Integer, nullable=False, doc="数量")
    status = Column(Integer, nullable=False, doc="订单状态")

    address_id = Column(Integer, nullable=True, doc="收货人信息")
    order_no = Column(String(30), nullable=True, doc="货物订单号")
    out_trade_no = Column(String(30), nullable=True, doc="统一支付订单号")
    cart_time = Column(TIMESTAMP, nullable=True, doc="加入购物车时间")
    pay_time = Column(TIMESTAMP, nullable=True, doc="付款时间")
    send_time = Column(TIMESTAMP, nullable=True, doc="发货时间")
    receive_time = Column(TIMESTAMP, nullable=True, doc="收货时间")
    complete_time = Column(TIMESTAMP, nullable=True, doc="确认完成时间")
    close_time = Column(TIMESTAMP, nullable=True, doc="关闭订单时间")
    close_type = Column(Integer, nullable=True, doc='订单被关闭的类型')
    is_del = Column(BOOLEAN, nullable=False, server_default='0', doc="逻辑删除, true(删除)|false(未删除)")
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_time = Column(TIMESTAMP, nullable=False, server_onupdate=text("CURRENT_TIMESTAMP"))

    STATUS_CART = 1
    STATUS_WAIT_PAY = 2
    STATUS_WAIT_SEND = 3
    STATUS_WAIT_RECEIVE = 4
    STATUS_COMPLETE = 5
    STATUS_CLOSE = 6

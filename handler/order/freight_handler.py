#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler, handler
import uuid
from model import OrderModel
from model import AddressModel
from model import CommodityModel
from model import OptionModel
from model import AttributeModel
import utils.config
from utils.exception import *
from wechatpy.pay import WeChatPay
from wechatpy.pay.api import WeChatOrder


class FreightHandler(BaseHandler):
    @handler
    def post(self):
        order_ids = self.get_json_argument('order_ids')
        address_id = self.get_json_argument('address_id')
        return {"freight": 5}

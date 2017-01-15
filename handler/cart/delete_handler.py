#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import datetime
from handler.base.base_handler import BaseHandler
import json
from handler.base.base_handler import BaseHandler, handler
import uuid
from model import ModelConfig
from model import CommodityModel
from model import AttributeModel
from model import UserModel
from model import OrderModel
from utils.exception import ServerError


class DeleteHandler(BaseHandler):
    @handler
    def post(self):
        order_ids = self.get_json_argument('order_ids')

        order_models = self.model_config.filter_all(OrderModel, user_id=1, status=OrderModel.STATUS_CART,
                                                    filters=OrderModel.order_no.in_(tuple(order_ids)))
        for order_model in order_models:  # type:OrderModel
            order_model.is_del = True
            order_model.status = OrderModel.STATUS_CLOSE
            order_model.close_type = OrderModel.STATUS_CART
            order_model.close_time = datetime.datetime.now()
        self.model_config.commit()
        order_models = self.model_config.all(OrderModel, user_id=1, status=OrderModel.STATUS_CART)
        res = {
            'cart_count': len(order_models),  # 购物袋中商品的数量
        }
        return res

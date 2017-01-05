#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
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
        model_config = ModelConfig()
        order_models = model_config.filter_all(OrderModel, user_id=1, status=OrderModel.STATUS_CART,
                                               filters=OrderModel.order_no.in_(tuple(order_ids)))
        for order_model in order_models:  # type:OrderModel
            order_model.is_del = True
            order_model.status = OrderModel.STATUS_CLOSE
        model_config.flush()
        model_config.commit()

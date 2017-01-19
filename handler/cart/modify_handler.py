#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler, handler
import uuid
from model import ModelConfig
from model import CommodityModel
from model import AttributeModel
from model import UserModel
from model import OrderModel
from utils.exception import ServerError
from model import OptionModel


class ModifyHandler(BaseHandler):
    @handler
    def post(self):
        order_id = self.get_json_argument('order_id')
        selected_option_ids = self.get_json_argument('selected_option_ids')
        count = self.get_json_argument('count')

        order_model = self.model_config.first(OrderModel, user_id=1, id=order_id)  # type:OrderModel
        if not order_model:
                raise ServerError(ServerError.ORDER_ID_ILLEGEL, args=order_id)
        commodity_id = order_model.commodity_id
        commodity_model = self.model_config.all(CommodityModel, id=commodity_id)
        attribute_models = self.model_config.all(AttributeModel, commodity_id=order_model.commodity_id)
        selected_option_models = self.model_config.filter_all(OptionModel,
                                                            OptionModel.id.in_(tuple(selected_option_ids)))
        selected_attr_names = []
        for selected_option_model in selected_option_models:  # type:OptionModel
            if selected_option_model.commodity_id != commodity_id:
                raise ServerError(ServerError.CART_ADD_IDS_NOT_MATCH)
            attribute_model = self.model_config.first(AttributeModel, id=selected_option_model.attr_id)
            selected_attr_names.append(attribute_model.attr_name)
        attr_names = []
        for attribute_model in attribute_models:  # type: AttributeModel
            attr_names.append(attribute_model.attr_name)
        if set(selected_attr_names) != set(attr_names):
            raise ServerError(ServerError.CART_ADD_IDS_NOT_MATCH)

        order_model = OrderModel(user_id=1, commodity_id=commodity_id,
                                 selected_option_ids=list(set(selected_option_ids)), count=count,
                                 status=OrderModel.STATUS_CART)
        self.model_config.add(order_model)
        return ''

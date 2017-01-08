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
from model import OptionModel


class GetHandler(BaseHandler):
    @handler
    def post(self):
        order_ids = self.get_json_argument('order_ids', default=[], allow_null=True)

        if not order_ids:
            order_models = self.model_config.all(OrderModel, user_id=1, status=OrderModel.STATUS_CART)
        else:
            order_models = self.model_config.filter_all(OrderModel, OrderModel.id.in_(tuple(order_ids)), user_id=1,
                                                        status=OrderModel.STATUS_CART,
                                                        )
        orders = []
        total_price = 0
        for order_model in order_models:  # type:OrderModel
            selected_option_ids = order_model.selected_option_ids
            commodity_id = order_model.commodity_id
            commodity_model = self.model_config.first(CommodityModel, id=commodity_id)  # type:CommodityModel
            selected_option_models = self.model_config.filter_all(OptionModel,
                                                                  OptionModel.id.in_(tuple(selected_option_ids)))
            options = []
            price = commodity_model.base_price
            for selected_option_model in selected_option_models:  # type:OptionModel
                selected_attribute_model = self.model_config.first(AttributeModel,
                                                                   id=selected_option_model.attr_id)  # type:CommodityModel
                options.append({
                    'attr_name': selected_attribute_model.attr_name,
                    'cn_attr_name': selected_attribute_model.cn_attr_name,
                    'option_name': selected_option_model.option_name,
                    'cn_option_name': selected_option_model.cn_option_name,
                    'option_id': selected_option_model.id
                })
                price += selected_option_model.weight
            total_price += price * order_model.count
            order = {
                'commodity_id': commodity_id,
                'order_id': order_model.id,
                'order_no': order_model.order_no,
                'commodity_title': commodity_model.title,
                'count': order_model.count,
                'options': options,
                'price': price * order_model.count

            }
            orders.append(order)
        res = {
            'total_price': total_price,
            'orders': orders
        }
        return res

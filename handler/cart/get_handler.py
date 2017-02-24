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
        immediately = self.get_json_argument('immediately', default=False, allow_null=True)

        if str(immediately).lower() == 'true':
            print immediately
            status = OrderModel.STATUS_ORDER_IMMEDIATELY
        else:
            status = OrderModel.STATUS_CART
        if not order_ids:
            order_models = self.model_config.all(OrderModel, user_id=1, status=status)
        else:
            order_models = self.model_config.filter_all(OrderModel, OrderModel.id.in_(tuple(order_ids)), user_id=1,
                                                        status=status,
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
                if selected_attribute_model.index == 1:
                    selected_first_option = selected_option_model.option_name
                price += selected_option_model.weight
            total_price += price * order_model.count
            order = {
                'commodity_id': commodity_id,
                'order_id': order_model.id,
                'order_no': order_model.order_no,
                'commodity_title': commodity_model.title,
                'count': order_model.count,
                'options': options,
                'thumbnail': '%s/preseller/img/commodity/%s/attribute/%s.jpg' % (
                    self.get_inner_static_path(), commodity_id, selected_first_option),
                'price': price * order_model.count

            }
            orders.append(order)
        res = {
            'total_price': round(total_price, 2),
            'orders': orders
        }
        return res

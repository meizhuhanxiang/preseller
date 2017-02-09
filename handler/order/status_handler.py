#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler, handler
from utils.exception import ServerError
from model import OrderModel
from model import CommodityModel
from model import OptionModel
from model import AttributeModel
from model import AddressModel


class StatusHandler(BaseHandler):
    @handler
    def post(self):
        order_status = self.get_json_argument('status')
        if order_status not in OrderModel.STATUS_LIST:
            raise ServerError(ServerError.ORDER_STATUS_ILLEGAL, args=order_status)
        if order_status == OrderModel.STATUS_ALL:
            order_models = self.model_config.all(OrderModel, user_id=1)
        else:
            order_models = self.model_config.all(OrderModel, user_id=1, status=order_status)

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
            payed_order_models = self.model_config.filter_all(OrderModel,
                                                              OrderModel.status.in_(tuple(OrderModel.STATUS_PAY_LIST)),
                                                              user_id=1, commodity_id=commodity_model.id)
            sold_count = len(payed_order_models)
            order = {
                'commodity_id': commodity_id,
                'order_id': order_model.id,
                'order_no': order_model.order_no,
                'commodity_title': commodity_model.title,
                'count': order_model.count,
                'options': options,
                'thumbnail': '/%s/preseller/img/commodity/%s/attribute/%s.jpg' % (
                    self.get_inner_static_path(), commodity_id, selected_first_option),
                'price': price * order_model.count,
                'status': order_model.status,
                'address_id': order_model.address_id,
                'presell_count': commodity_model.presell_count,  # 总共想预售的数量
                'sold_count': sold_count,  # 已经卖的数量
                'satisfy_count': commodity_model.satisfy_count,  # 满多少件发货
                'stop_sell': False

            }
            orders.append(order)
        res = {
            'orders': orders
        }
        return res

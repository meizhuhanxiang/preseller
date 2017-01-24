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
from utils.exception import ServerError


class AddHandler(BaseHandler):
    @handler
    def post(self):
        if not self.session.get('open_id', ''):
            raise ServerError(ServerError.USER_NO_LOGIN)
        order_ids = self.get_json_argument('order_ids')
        address_id = self.get_json_argument('address_id')
        out_trade_no = str(uuid.uuid1()).replace('-', '')
        total_price = 0
        desc = []
        for order_id in order_ids:
            order_model = self.model_config.first(OrderModel, user_id=1, id=order_id,
                                                  status=OrderModel.STATUS_CART)  # type: OrderModel
            if not order_model:
                raise ServerError(ServerError.ORDER_ID_ILLEGEL, args=order_id)
            selected_option_ids = order_model.selected_option_ids
            commodity_id = order_model.commodity_id
            commodity_model = self.model_config.first(CommodityModel, id=commodity_id)  # type:CommodityModel
            selected_option_models = self.model_config.filter_all(OptionModel,
                                                                  OptionModel.id.in_(tuple(selected_option_ids)))
            price = commodity_model.base_price
            desc.append(commodity_model.title)
            for selected_option_model in selected_option_models:  # type:OptionModel
                price += selected_option_model.weight
            total_price += price * order_model.count
            order_model.out_trade_no = out_trade_no
            order_model.address_id = address_id
        desc = ','.join(desc)
        if len(desc) >= 100:
            desc = '%s...' % desc[:100]
        body = u'棒棒预售-%s' % desc
        web_url = utils.config.get('global', 'url')
        wechat_conf = utils.config.get_section('wechat')
        app_id = wechat_conf['appid']
        key = wechat_conf['key']
        mchid = wechat_conf['mchid']
        mch_cert = wechat_conf['mch_cert']
        mch_key = wechat_conf['mch_key']
        wechat_order_client = WeChatPay(app_id, key, mchid, mch_cert=mch_cert,
                                        mch_key=mch_key).order  # type:WeChatOrder
        uni_res = wechat_order_client.create('JSAPI', body, 1,
                                             '%s/api/order/notify' % web_url,
                                             user_id=self.session['open_id'], out_trade_no=out_trade_no)
        appapi_params = wechat_order_client.get_appapi_params(uni_res['prepay_id'])
        res = {
            'appapi_params': appapi_params,
            'out_trade_no': out_trade_no
        }
        return res

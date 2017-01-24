#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler
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


class NotifyHandler(BaseHandler):
    def post(self):
        web_url = utils.config.get('global', 'url')
        wechat_conf = utils.config.get_section('wechat')
        app_id = wechat_conf['appid']
        key = wechat_conf['key']
        mchid = wechat_conf['mchid']
        mch_cert = wechat_conf['mch_cert']
        mch_key = wechat_conf['mch_key']
        wechat_order_client = WeChatPay(app_id, key, mchid)
        try:
            wechat_data = wechat_order_client.parse_payment_result(self.request.body)
            result_code = wechat_data.get('result_code', '')
            return_code = wechat_data.get('return_code', '')
            out_trade_no = wechat_data.get('out_trade_no', '')
            if result_code != 'SUCCESS' or return_code != 'SUCCESS' or not out_trade_no:
                print '支付失败'
            else:
                print '支付成功'
            order_client = wechat_order_client.order
            query_data = order_client.query(out_trade_no=out_trade_no)
            print query_data, '=========='
        except Exception, e:
            self.logger.info(e)



#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import datetime
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
        SUCCESS, FAIL = "SUCCESS", "FAIL"
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
                self.logger.error('pay failed!!!')
                self.write(FAIL)
            else:
                order_client = wechat_order_client.order
                query_data = order_client.query(out_trade_no=out_trade_no)
                if query_data:
                    order_models = self.model_config.all(OrderModel, user_id=1, out_trade_no=out_trade_no)
                    for order_model in order_models:  # type:OrderModel
                        order_model.status = OrderModel.STATUS_WAIT_SEND
                        order_model.pay_time = datetime.datetime.now()
                    if order_models:
                        self.model_config.commit()
                        self.logger.info('pay success!!!')
                        self.write(SUCCESS)
                    else:
                        self.logger.error('pay failed!!!')
                        self.write(FAIL)
                else:
                    self.logger.error('pay failed!!!')
                    self.write(FAIL)
                    # OrderedDict([(u'return_code', u'SUCCESS'), (u'return_msg', u'OK'), (u'appid', u'wx1f5f84b210348212'), (u'mch_id', u'1377692402'), (u'nonce_str', u'jLutLne3WcsmaAId'), (u'sign', u'2FEBA18A99702C3667EA3CCE838FE2AD'), (u'result_code', u'SUCCESS'), (u'openid', u'oZDZcxIVPgABuLIbLi_ZEENVRzGM'), (u'is_subscribe', u'Y'), (u'trade_type', u'JSAPI'), (u'bank_type', u'CFT'), (u'total_fee', u'1'), (u'fee_type', u'CNY'), (u'transaction_id', u'4007362001201702038556330643'), (u'out_trade_no', u'31a63b3ae9e011e6a05bfa163ec98286'), (u'attach', None), (u'time_end', u'20170203151305'), (u'trade_state', u'SUCCESS'), (u'cash_fee', u'1')])

        except Exception, e:
            self.logger.error(e)

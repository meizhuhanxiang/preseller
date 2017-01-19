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


class AddHandler(BaseHandler):
    def post(self):
        order_ids = self.get_json_argument('orderids')
        address_id = self.get_json_argument('address_id')
        out_trade_no = uuid.uuid1().replace('-', '')
        total_price = 0
        desc = []
        for order_id in order_ids:
            order_model = self.model_config.first(OrderModel, user_id=1, order_id=order_id,
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
        wechat_conf = utils.config.get_section('wechat')
        app_id = wechat_conf['appid']
        app_secret = wechat_conf['appsecret']
        mchid = wechat_conf['mchid']
        wechat_order_client = WeChatPay(app_id, app_secret, mchid).order  # type:WeChatOrder
        """
        统一下单接口

        :param trade_type: 交易类型，取值如下：JSAPI，NATIVE，APP，WAP
        :param body: 商品描述
        :param total_fee: 总金额，单位分
        :param notify_url: 接收微信支付异步通知回调地址
        :param client_ip: 可选，APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
        :param user_id: 可选，用户在商户appid下的唯一标识。trade_type=JSAPI，此参数必传
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :param detail: 可选，商品详情
        :param attach: 可选，附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
        :param fee_type: 可选，符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param time_start: 可选，订单生成时间，默认为当前时间
        :param time_expire: 可选，订单失效时间，默认为订单生成时间后两小时
        :param goods_tag: 可选，商品标记，代金券或立减优惠功能的参数
        :param product_id: 可选，trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义
        :param device_info: 可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        :param limit_pay: 可选，指定支付方式，no_credit--指定不能使用信用卡支付
        :return: 返回的结果数据

        trade_type, body, total_fee, notify_url, client_ip=None,
               user_id=None, out_trade_no=None, detail=None, attach=None,
               fee_type='CNY', time_start=None, time_expire=None,
               goods_tag=None, product_id=None, device_info=None, limit_pay=None
        """

        wechat_order_client.create('JSAPI', body, total_price, )

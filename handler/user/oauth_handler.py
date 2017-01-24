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
from wechatpy.oauth import WeChatOAuth


class OauthHandler(BaseHandler):
    def get(self):
        current_url = self.get_argument('current_url', '')
        self.session['current_url'] = current_url
        print current_url, '===='
        web_url = utils.config.get('global', 'url')
        wechat_conf = utils.config.get_section('wechat')
        app_id = wechat_conf['appid']
        app_secret = wechat_conf['appsecret']
        web_url = utils.config.get('global', 'url')
        callback_url = '%s/api/user/callback' % web_url
        urls = 'http://www.gsteps.cn/Home/Oauth/get_wx_code' \
               '?appid=%s' \
               '&scope=snsapi_userinfo' \
               '&state=callback' \
               '&redirect_uri=%s' % (
                   app_id, callback_url)
        self.session.save()
        self.redirect(urls)

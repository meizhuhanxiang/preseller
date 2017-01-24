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


class CallbackHandler(BaseHandler):
    def get(self):
        code = self.get_argument('code')
        state = self.get_argument('state')
        wechat_conf = utils.config.get_section('wechat')
        app_id = wechat_conf['appid']
        app_secret = wechat_conf['appsecret']
        web_url = utils.config.get('global', 'url')
        oauth_client = WeChatOAuth(app_id, app_secret, '')
        access_token = oauth_client.fetch_access_token(code)
        self.session['open_id'] = oauth_client.open_id
        user_info =  oauth_client.get_user_info()
        if self.session.has_key('current_url'):
            current_url = self.session.get('current_url')
            self.session['current_url'] = ''
            self.session.save()
            self.redirect(current_url)
        else:
            self.redirect(web_url)

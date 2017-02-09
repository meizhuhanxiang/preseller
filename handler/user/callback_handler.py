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
from model import UserModel
import urllib


class CallbackHandler(BaseHandler):
    def get(self):
        code = self.get_argument('code')
        state = self.get_argument('state')
        wechat_conf = utils.config.get_section('wechat')
        app_id = wechat_conf['appid']
        app_secret = wechat_conf['appsecret']
        web_url = utils.config.get('global', 'url')
        oauth_client = WeChatOAuth(app_id, app_secret, '')
        oauth_client.fetch_access_token(code)

        user_info = oauth_client.get_user_info()
        self.session['open_id'] = user_info['openid']
        user_model = self.model_config.first(UserModel, open_id=user_info['openid'])  # type:UserModel
        if user_model:
            user_model.profile = user_info['headimgurl']
            user_model.nickname = user_info['nickname']
            self.model_config.commit()
        else:
            user_model = UserModel(nickname=user_info['nickname'],
                                   open_id=user_info['openid'],
                                   sex=user_info['sex'],
                                   province=user_info['province'],
                                   country=user_info['country'],
                                   city=user_info['city'],
                                   profile=user_info['headimgurl'],
                                   privilege=user_info['privilege'],
                                   union_id=user_info['unionid']
                                   )
            self.model_config.add(user_model)
        self.session.save()
        if self.session.get('current_url', ''):
            current_url = urllib.unquote_plus(self.session.get('current_url'))
            self.session['current_url'] = ''
            self.session.save()
            self.logger.info('current_url:%s' % current_url)
            self.redirect(current_url)
        else:
            self.logger.info('current_url:   null')
            self.redirect(web_url)

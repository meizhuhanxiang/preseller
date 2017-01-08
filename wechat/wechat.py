# coding: utf-8
import os
import time
import hashlib
import urllib
import functools
import urllib2
import json
from model.indance_handler import InDanceDB
import utils.config
import requests
from model.cache_handler import WechatCacheDB
from utils.code import *
from utils.logger import runtime_logger

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'

BASE_TOKEN = 1
WX_TICKET = 2
NONCESTR = 'Wm3WZYTPz0wzccnW'


def oauth(method):
    @functools.wraps(method)
    def warpper(self, *args, **kwargs):
        if not self.session.has_key('union_id'):
            self.session['current_url'] = self.request.uri
            self.session.save()
            callback_url = urllib.quote_plus(os.path.join(self.domain, 'wechat/callback'))
            urls = self.wechat.get_oauth_url(callback_url)
            self.redirect(urls)
        else:
            method(self, *args, **kwargs)

    return warpper


class WeChat(object):
    def __init__(self):
        self.appid = utils.config.get('wechat', 'appid')
        self.token = utils.config.get('wechat', 'token')
        self.appsecret = utils.config.get('wechat', 'appsecret')
        self.mchid = utils.config.get('wechat', 'mchid')
        self.notify_url = utils.config.get('wechat', 'notify_url')
        self.share_domain = utils.config.get('global', 'share_domain')
        self.cache_talbe = utils.config.get('wechat_cache', 'table')

    def url_get(self, urls, data=None):
        req = urllib2.Request(urls, data=data)
        response = urllib2.urlopen(req)
        return json.loads(response.read())

    def get_oauth_url(self, callback_url):
        urls = 'http://www.gsteps.cn/Home/Oauth/get_wx_code?appid=%s&scope=snsapi_userinfo&state=callback&redirect_uri=%s' % (
            self.appid, callback_url)
        return urls

    def get_access_token(self, code):
        code_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' \
                   'appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (self.appid, self.appsecret, code)
        res = self.url_get(code_url)
        access_token = res['access_token']
        print 'first get', access_token
        union_id = res['unionid']
        self.open_id = res['openid']
        self.access_token = access_token
        self.union_id = union_id
        return access_token

    def get_user_info(self):
        urls = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (
            self.access_token, self.open_id)
        # urls = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (
        #     self.get_base_access_token(InDanceDB()), self.open_id)
        res = self.url_get(urls)
        runtime_logger().info(res)
        user_info = {
            'open_id': res['openid'],
            'nickname': res['nickname'],
            'sex': res['sex'],
            'province': res['province'],
            'city': res['city'],
            'country': res['country'],
            'head_img_url': res['headimgurl'],
            'privilege': res['privilege'],
            'union_id': res['unionid']
        }
        self.user_info = user_info
        return user_info

    def get_base_access_token(self, db):
        cache_info = db.get_cache(BASE_TOKEN)
        code = cache_info['code']
        access_token = cache_info['cache']
        if code != SUCCESS:
            urls = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
                self.appid, self.appsecret)
            res = self.url_get(urls)
            access_token = res.get('access_token', '')
            if access_token:
                db.save_cache(access_token, BASE_TOKEN)
        return access_token

    def get_wx_ticket(self, db):
        cache_info = db.get_cache(WX_TICKET)
        code = cache_info['code']
        wx_ticket = cache_info['cache']
        if code != SUCCESS:
            urls = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" % self.get_base_access_token(db)
            res = self.url_get(urls)
            wx_ticket = res.get('ticket', '')
            if wx_ticket:
                db.save_cache(wx_ticket, WX_TICKET)
        return wx_ticket

    def get_menu_share_conf(self, share_url, db):
        runtime_logger().info('jsapi_ticket:---------------')
        wechat_cache = WechatCacheDB('wechat_cache')
        jsapi_ticket = wechat_cache.get_cache(WX_TICKET, self.cache_talbe)
        runtime_logger().info('jsapi_ticket:%s' % jsapi_ticket)
        timestamps = int(time.time())
        s = 'jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s' % (jsapi_ticket, NONCESTR, timestamps, share_url)
        signature = hashlib.sha1(s).hexdigest()
        return json.dumps({'appid': self.appid,
                           'timestamp': timestamps,
                           'noncestr': NONCESTR,
                           'signature': signature,
                           'link': share_url,
                           'js_api_list': ['onMenuShareTimeline', 'onMenuShareAppMessage'],
                           'signature_decode': s
                           })
        #
        # @app.route('/conf_menu_share', methods=['get'])
        # def conf_menu_share():
        #     url = '%s/?union_id=%s' % (DOMAIN, session.get('union_id', ''))
        #     return get_menu_share_conf(url)

    def pay_unifiedorder(self):
        urls = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

    def send_template(self, **args):
        access_token = args.get('access_token', '')
        open_id = args.get('open_id', '')
        db = args.get('db', '')
        first = args.get('first', '')
        keyword1 = args.get('keyword1', '')
        keyword2 = args.get('keyword2', '')
        keyword3 = args.get('keyword3', '')
        keyword4 = args.get('keyword4', '')
        detail_url = args.get('urls', '')
        runtime_logger().info('detail_url:%s' % detail_url)
        remart = args.get('remark', '')
        wechat_cache = WechatCacheDB('wechat_cache')
        base_token = wechat_cache.get_cache(BASE_TOKEN, self.cache_talbe)
        runtime_logger().info('base_token:%s' % base_token)
        urls = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % base_token
        data = {
            "touser": open_id,
            "template_id": "0vii4KFKNwCc-J_SG9hLswhnxhJzq7HghXWTJPv2oZU",
            "url": detail_url,
            "topcolor": "#FF0000",
            "data": {
                "first": {
                    "value": first,
                    "color": "#173177"
                },
                "keyword1": {
                    "value": keyword1,
                    "color": "#173177"
                },
                "keyword2": {
                    "value": keyword2,
                    "color": "#173177"
                },
                "keyword3": {
                    "value": keyword3,
                    "color": "#173177"
                },
                "keyword4": {
                    "value": keyword4,
                    "color": "#173177"
                },
                "remark": {
                    "value": remart,
                    "color": "#173177"
                }
            }
        }
        return self.url_get(urls, json.dumps(data))
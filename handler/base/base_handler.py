#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import json
import tornado.web
import tornado.ioloop
import tornado.options
import utils.config
import tornado.httpserver
from functools import wraps
from traceback import format_exc
from utils.exception import *
from utils.logger import api_logger
from model import ModelConfig
from utils import session


def handler(fun):
    @wraps(fun)
    def wrapper(self, *args, **kwargs):
        code, msg, res = 0, 'success', None
        try:
            # if not self.session.get('open_id', ''):
            #     if self.__class__.__name__ != 'CheckloginHandler':
            #         raise ServerError(ServerError.USER_NO_LOGIN)
            res = fun(self, *args, **kwargs)
        except BaseError, e:
            code, msg = e.split()
        except Exception, e:
            self.logger.error(format_exc())
            code, msg = 65535, 'UnHandler Error: {e}'.format(e=str(e))
        resp = {'code': code, 'msg': u'%s' % msg, 'res': res}
        resp = json.dumps(resp)
        api_logger().info(
            '%s: %s' % (self.__class__.__name__, re.sub(r'(\\n|\\|\s+)', '', resp)))
        self.write(resp)

    return wrapper


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    def initialize(self):
        self.model_config = ModelConfig()
        self.get_secure_cookie("session_id")
        self.session = session.Session(self.application.session_manager, self)
        self.logger = api_logger()
        self.logger.info(
            '%s: %s' % (self.__class__.__name__, re.sub(r'(\\n|\\|\s+)', '', json.dumps(self.request.body))))

    def on_finish(self):
        self.model_config.close()

    def get_need_args(self, args):
        res = {}
        for arg in args:
            try:
                param = self.get_argument(arg)
                res[arg] = param
            except:
                raise ServerError(ServerError.ARGS_MISSING, args=arg)
        return res

    def get_inner_static_path(self):
        return utils.config.get('global', 'inner_static')

    def get_json_argument(self, name, default=None, allow_null=False):
        r_body = self.request.body
        if not r_body:
            r_body = '{}'
        request_body = json.loads(r_body)
        if name not in request_body and not allow_null:
            raise ServerError(ServerError.ARGS_MISSING, args=name)
        return request_body.get(name, default)

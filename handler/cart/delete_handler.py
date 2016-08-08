#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class DeleteHandler(BaseHandler):
    def post(self):
        # 期望接收到的post_json
        # ['asfasdf', 'asdf'] #想要从购物车中删除的cart_id列表

        res = {
        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write({'reason': '', 'res': res})
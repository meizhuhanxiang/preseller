#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class DeleteHandler(BaseHandler):
    def post(self):
        # 期望接收到的post_json
        # {'codes':['123465789542525', '223465789543242']}
        res = {}
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({'reason': '', 'res': res}))

#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class DeleteHandler(BaseHandler):
    def post(self):
        # 期望接收到的post_json
        # 删除地址时
        # {
        #     'ddl':'delete'   #值必须是delete
        #     'address_id': 1 # 地址id,整个系统唯一
        # }
        res = {}

        id = self.get_argument('address_id')
        res = {'address_id': 'sadfasdf'}
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({'reason': '', 'res': res}))

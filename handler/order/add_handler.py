#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class AddHandler(BaseHandler):
    def post(self):
        # 期望接收的数据
        # {
        #     'cart_ids': [
        #         'xxxx',
        #         'yyyy'
        #     ],
        #     'address_id': '3423',  # 物流信息id可以根据该id获取物流详细细信息
        # }
        self.write({'reason': '', 'res': ''})

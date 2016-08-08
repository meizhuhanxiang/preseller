#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class AddHandler(BaseHandler):
    def post(self, seed_id):
        # 期望接收到的post_json
        # {
        #     'count':1, # 数量
        #     'seed_id': 'dfsadfasdf',
        #     'properties': [
        #         {
        #             'name': '颜色',
        #             'type': '黑色'
        #         },
        #         {
        #             'name': '大小',
        #             'type': 'S'
        #         },
        #         {
        #             'name': '其他',
        #             'type': 't1'
        #         }
        #     ]
        # }
        res = {
            'cart_id': '123465789542525',  # 返回商品的订单id
            'seed_id': 'dfsadfasdf',
            'cart_count': 10  # 购物车中商品总数量
        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write({'reason': '', 'res': res})

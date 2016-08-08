#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class AllHandler(BaseHandler):
    def get(self):
        res = {
            'cart_count': 10,  # 购物车中商品总数量
            'cart': [
                {
                    'cart_id': '123465789542525',  # 返回商品的订单id
                    'seed_id': 'df342sdfsdf',  # 商品id
                    'count': 10,  # 商品数量
                    'price': '456',  # 单价
                    'total_price': '4560',  # 总价
                    'unit': '1',
                    'properties': [
                        {
                            'name': '颜色',
                            'type': '黑色'
                        },
                        {
                            'name': '大小',
                            'type': 'S'
                        },
                        {
                            'name': '其他',
                            'type': 't1'
                        }
                    ]
                }
            ]
        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write({'reason': '', 'res': res})

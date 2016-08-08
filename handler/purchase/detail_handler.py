#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class DetailHandler(BaseHandler):
    def get(self, seed_id):
        res = {
            'navigation_img': 'img/navigation.jpg',
            'thumbnails': 'img/thumbnails.jpg',
            'name': 'G-STEP冬季卫衣',
            'price': '456',
            'unit': '1',
            'properties': [
                {
                    'name': '颜色',
                    'type': ['黑色', '白色', '草青色', '红色', '蓝色']
                },
                {
                    'name': '大小',
                    'type': ['S', 'M', 'L', 'XL', 'XXL']
                },
                {
                    'name': '其他',
                    'type': ['t1', 't2', 't3', 't4', 't5']
                }
            ]
        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({'reason': '', 'res': res}))

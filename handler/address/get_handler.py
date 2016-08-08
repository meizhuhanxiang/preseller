#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class GetHandler(BaseHandler):
    def post(self):
        # 期待接收的参数
        # ['address_id1', 'address_id2'] # 列表
        res = [
            {
                'name': '范晓宇',
                'country': '中国',
                'province': '北京市',
                'region': '朝阳区',
                'address': '酒仙桥6号院电子国际总部',
                'phone': '13552266949',
                'default': 1,  # 默认收获地址
                'address_id': 1,  # 地址id,整个系统唯一
            },
            {
                'name': '李颖',
                'country': '中国',  # 国家
                'province': '北京市',  # 省(直辖市)
                'region': '朝阳区',  # 县(区)
                'address': '酒仙桥6号院电子国际总部',  # 具体地址
                'phone': '18966677772',
                'default': 0,  # 非默认收获地址
                'address_id': 2,  # 地址id,整个系统唯一
            }
        ]
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({'reason': '', 'res': res}))

#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class ModifyHandler(BaseHandler):
    def post(self):
        # 期望接收到的post_json
        # 修改地址时:
        # {
        #     'ddl':'change'   #值必须是change
        #     'name': '李颖',
        #     'country': '中国',  # 国家
        #     'province': '北京市',  # 省(直辖市)
        #     'region': '朝阳区',  # 县(区)
        #     'address': '酒仙桥6号院电子国际总部',  # 具体地址
        #     'phone': '18966677772',
        #     'default': 0,  # 非默认收获地址
        #     'address_id': 2,  # 地址id,整个系统唯一
        # }
        res = {}
        address_id = self.get_argument('address_id')
        name = self.get_argument('name')
        country = self.get_argument('country')
        province = self.get_argument('province')
        region = self.get_argument('region')
        address = self.get_argument('address')
        phone = self.get_argument('phone')
        default = self.get_argument('phone')
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({'reason': '', 'res': res}))

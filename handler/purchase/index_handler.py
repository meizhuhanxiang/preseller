#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):
        res = {
            'seed_id': 'xxxxx',  # 商品id
            'title': 'G-STEPS卫衣预售',
            'brief': '360程序员做的衣服好看又耐穿',
            'navigation': '/image/profile1.png',
            'presell_count': 100,  # 总共想预售的数量
            'sold_count': 68,  # 已经卖的数量
            'satisfy_count': 20,  # 满多少件发货
            'logo': '/image/profile2.png',
            'publisher': 'G-STEPS街舞社',
            'cart_count': 5,  # 购物袋中商品的数量
            'seed_id': 'aaaaaaaaaaa',  # 商品id（注意这个不是订单id）
            'recommends': [{
                'profile': '/image/profile1.png',
                'name': '刘怡君',
                'job': '360产品经理',
                'is_v': 1,
                'content': '360程序员街舞社，特别靠谱的一个团队做的衣服，之前就买过，面料贼好！'
            },
                {
                    'profile': '/image/profile2.png',
                    'name': '张敏',
                    'job': '京东高级产品经理/产品主管',
                    'is_v': 1,
                    'content': '终于又出衣服啦！上次就买过，也查过同样质量的衣服，淘宝卖170，真的推荐大家买！'
                }],

        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({'reason': '', 'res': res}))

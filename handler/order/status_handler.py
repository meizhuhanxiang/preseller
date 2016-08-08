#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class StatusHandler(BaseHandler):
    # order_status  wait_pay(代付款)、wait_send(待发货)、wait_receive(待收货)、complete(已完成)、all(全部)、close(已关闭)
    def get(self, order_status):
        statuses = ['wait_pay', 'wait_send', 'wait_receive', 'complete', 'close']
        order_statuses = [order_status, order_status]
        if order_status == 'all':
            import random
            order_statuses = [statuses[random.randint(0, 4)], statuses[random.randint(0, 4)]]
        res = [
            {
                'code': '123465789542525',  # 订单编码
                'name': 'G-STEP冬季卫衣',
                'thumbnails': 'img/thumbnails2.jpg',  # 小缩略图
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
                    },
                ],
                'price': '490.5',
                'count': 1,  # 商品个数
                'time': '2019-12-12 02:23:14',  # 该订单变更为当前状态的时间
                'address_id': '3453',  # 物流信息id可以根据该id获取物流详细细信息
                'order_status': order_statuses[0],  # 订单状态
                'presell_count': 100,  # 总共想预售的数量
                'sold_count': 68,  # 已经卖的数量
                'satisfy_count': 20,  # 满多少件发货
                'seed_id': 'aaaaaaaaa'  # 商品id,由系统后台确定且唯一
            },
            {
                'code': '223465789543242',
                'name': 'G-STEP门票',
                'thumbnails': 'img/thumbnails2.jpg',
                'properties': [
                    {
                        'name': '排',
                        'type': '4'
                    },
                    {
                        'name': '列',
                        'type': '2'
                    },
                    {
                        'name': '区域',
                        'type': '1'
                    },
                ],
                'price': '50',
                'count': 5,  # 商品数量
                'time': '2019-12-12 02:23:14',  # 该订单变更为当前状态的时间
                'address_id': '3432',  # 物流信息id可以根据该id获取物流详细细信息
                'order_status': order_statuses[1],  # wait_pay(代付款)、wait_send(待发货)、wait_receive(待收货)、已完成
                'presell_count': 100,  # 总共想预售的数量
                'sold_count': 68,  # 已经卖的数量
                'satisfy_count': 20,  # 满多少件发货
                'seed_id': 'aaaaaaaaa'  # 商品id,由系统后台确定且唯一
            }
        ]
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({'reason': '', 'res': res}))

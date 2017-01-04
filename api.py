#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from tornado.options import define, options

define("port", default=10001, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Content-type", "application/json")


class CommodityIndexHandler(BaseHandler):
    def get(self, seed_id):
        res = {
            "title": "G-STEPS卫衣预售",
            "brief": "360程序员做的衣服好看又耐穿",
            "navigation": "/image/profile1.png",
            "presell_count": 100,  # 总共想预售的数量
            "sold_count": 68,  # 已经卖的数量
            "satisfy_count": 20,  # 满多少件发货
            "logo": "/image/profile2.png",
            "publisher": "G-STEPS街舞社",
            "cart_count": 5,  # 购物袋中商品的数量
            "seed_id": "aaaaaaaaaaa",  # 商品id（注意这个不是订单id）
            "recommends": [{
                "profile": "/image/profile1.png",
                "name": "刘怡君",
                "job": "360产品经理",
                "is_v": 1,
                "content": "360程序员街舞社，特别靠谱的一个团队做的衣服，之前就买过，面料贼好！"
            },
                {
                    "profile": "/image/profile2.png",
                    "name": "张敏",
                    "job": "京东高级产品经理/产品主管",
                    "is_v": 1,
                    "content": "终于又出衣服啦！上次就买过，也查过同样质量的衣服，淘宝卖170，真的推荐大家买！"
                }],

        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({"reason": "", "res": res}))


class RecommendHandler(BaseHandler):
    def get(self, seed_id):
        res = [
            {
                "profile": "/image/profile1.png",
                "name": "刘怡君",
                "job": "360产品经理",
                "is_v": 1,
                "content": "360程序员街舞社，特别靠谱的一个团队做的衣服，之前就买过，面料贼好！"
            },
            {
                "profile": "/image/profile2.png",
                "name": "张敏",
                "job": "京东高级产品经理/产品主管",
                "is_v": 1,
                "content": "终于又出衣服啦！上次就买过，也查过同样质量的衣服，淘宝卖170，真的推荐大家买！"
            },
        ]
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({"reason": "", "res": res}))


class PublisherHandler(BaseHandler):
    def get(self, seed_id):
        # a = self.get_argument("noun1")
        res = {
            "navigation_img": "/img/navigation_img.jpg",
            "brief_introduction": "我们的设计师都来自各个互联网公司的顶尖成员，都热爱hip-hop这个文化，我们以hip-hop为主题进行设计，以嘻哈的态度表达我们的生活，希望你能同感",
            "guarantee": "我们与广东的几个不错的加工厂有长期合作，她们代工的产品，在淘宝上一般都在200元左右，我们试穿了很长时间，认为比较靠谱，如果你认为不好，只要能指出问题，我们包退哦",
            "activity_photos": [
                "/img/activity_photo1.jpg",
                "/img/activity_photo2.jpg",
                "/img/activity_photo3.jpg",
            ]
        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({"reason": "", "res": res}))


class PurchaseDetailHandler(BaseHandler):
    def get(self, seed_id):
        res = {
            "navigation_img": "img/navigation.jpg",
            "thumbnails": "img/thumbnails.jpg",
            "name": "G-STEP冬季卫衣",
            "price": "456",
            "unit": "1",
            "properties": [
                {
                    "name": "颜色",
                    "type": ["黑色", "白色", "草青色", "红色", "蓝色"]
                },
                {
                    "name": "大小",
                    "type": ["S", "M", "L", "XL", "XXL"]
                },
                {
                    "name": "其他",
                    "type": ["t1", "t2", "t3", "t4", "t5"]
                }
            ]
        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({"reason": "", "res": res}))


class CartAddHandler(BaseHandler):
    def post(self, seed_id):
        # 期望接收到的post_json
        # {
        #     "count":1, # 数量
        #     "seed_id": "dfsadfasdf",
        #     "properties": [
        #         {
        #             "name": "颜色",
        #             "type": "黑色"
        #         },
        #         {
        #             "name": "大小",
        #             "type": "S"
        #         },
        #         {
        #             "name": "其他",
        #             "type": "t1"
        #         }
        #     ]
        # }
        res = {
            "cart_id": "123465789542525",  # 返回商品的订单id
            "seed_id": "dfsadfasdf",
            "cart_count": 10  # 购物车中商品总数量
        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write({"reason": "", "res": res})


class CartDeleteHandler(BaseHandler):
    def post(self):
        # 期望接收到的post_json
        # ["asfasdf", "asdf"] #想要从购物车中删除的cart_id列表

        res = {
        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write({"reason": "", "res": res})


class CartModifyHandler(BaseHandler):
    def post(self):
        # 期望接收到的post_json
        # {
        #     "cart_id": "123465789542525",
        #     "seed_id": "dfsadfasdf",
        #     "count":1, # 数量
        #     "properties": [
        #         {
        #             "name": "颜色",
        #             "type": "黑色"
        #         },
        #         {
        #             "name": "大小",
        #             "type": "S"
        #         },
        #         {
        #             "name": "其他",
        #             "type": "t1"
        #         }
        #     ]
        # }
        res = {
            "cart_id": "123465789542525"  # 返回购物车id
        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write({"reason": "", "res": res})


class CartAllHandler(BaseHandler):
    def get(self):
        res = {
            "cart_count": 10,  # 购物车中商品总数量
            "cart": [
                {
                    "cart_id": "123465789542525",  # 返回商品的订单id
                    "seed_id": "df342sdfsdf",  # 商品id
                    "count": 10,  # 商品数量
                    "price": "456",  # 单价
                    "total_price": "4560",  # 总价
                    "unit": "1",
                    "properties": [
                        {
                            "name": "颜色",
                            "type": "黑色"
                        },
                        {
                            "name": "大小",
                            "type": "S"
                        },
                        {
                            "name": "其他",
                            "type": "t1"
                        }
                    ]
                }
            ]
        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write({"reason": "", "res": res})


class CartDetailHandler(BaseHandler):
    def post(self):
        # 期待收到的json
        # ["cart_id1"]  #需要提供cart_id列表

        res = [
            {
                "cart_id": "123465789542525",  # 返回商品的订单id
                "seed_id": "df342sdfsdf",  # 商品id
                "count": 10,  # 商品数量
                "price": "456",  # 单价
                "total_price": "4560",  # 总价
                "unit": "1",
                "properties": [
                    {
                        "name": "颜色",
                        "type": "黑色"
                    },
                    {
                        "name": "大小",
                        "type": "S"
                    },
                    {
                        "name": "其他",
                        "type": "t1"
                    }
                ]
            }
        ]
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write({"reason": "", "res": res})


class OrderAddHandler(BaseHandler):
    def post(self):
        # 期望接收的数据
        # {
        #     "cart_ids": [
        #         "xxxx",
        #         "yyyy"
        #     ],
        #     "address_id": "3423",  # 物流信息id可以根据该id获取物流详细细信息
        # }
        self.write({"reason": "", "res": ""})


class OrderGetHandler(BaseHandler):
    def post(self):
        # 期望接收到的post_json
        # {"codes":["123465789542525", "223465789543242"]}
        res = [
            {
                "cart_id": "123465789542525",  # 购物车id
                "seed_id": "dfasfdsafefas",  # 购物车id
                "name": "G-STEP冬季卫衣",
                "thumbnails": "img/thumbnails2.jpg",  # 小缩略图
                "properties": [
                    {
                        "name": "颜色",
                        "type": "黑色"
                    },
                    {
                        "name": "大小",
                        "type": "S"
                    },
                    {
                        "name": "其他",
                        "type": "t1"
                    },
                ],
                "price": "490.5",
                "count": 1,  # 商品数量
                "time": "2019-12-12 02:23:14",  # 该订单变更为当前状态的时间
                "address_id": "123",  # 物流信息id可以根据该id获取物流详细细信息
                "order_status": "wait_pay",  # 订单状态
                "presell_count": 100,  # 总共想预售的数量
                "sold_count": 68,  # 已经卖的数量
                "satisfy_count": 20,  # 满多少件发货
                "seed_id": "aaaaaaaaa"  # 商品id,由系统后台确定且唯一
            },
            {
                "cart_id": "223465789543242",
                "seed_id": "dfasfasfefs",
                "name": "G-STEP门票",
                "thumbnails": "img/thumbnails2.jpg",
                "properties": [
                    {
                        "name": "排",
                        "type": "4"
                    },
                    {
                        "name": "列",
                        "type": "2"
                    },
                    {
                        "name": "区域",
                        "type": "1"
                    },
                ],
                "price": "50",
                "count": 5,  # 商品数量
                "time": "2019-12-12 02:23:14",  # 该订单变更为当前状态的时间
                "address_id": "23424",  # 物流信息id可以根据该id获取物流详细细信息
                "order_status": "wait_pay",  # wait_pay(代付款)、wait_send(待发货)、wait_receive(待收货)、已完成
                "presell_count": 100,  # 总共想预售的数量
                "sold_count": 68,  # 已经卖的数量
                "satisfy_count": 20,  # 满多少件发货
                "seed_id": "aaaaaaaaa"  # 商品id,由系统后台确定且唯一
            }
        ]
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({"reason": "", "res": res}))


class OrderDeleteHandler(BaseHandler):
    def post(self):
        # 期望接收到的post_json
        # {"codes":["123465789542525", "223465789543242"]}
        res = {}
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({"reason": "", "res": res}))


class OrderStatusHandler(BaseHandler):
    # order_status  wait_pay(代付款)、wait_send(待发货)、wait_receive(待收货)、complete(已完成)、all(全部)、close(已关闭)
    def get(self, order_status):
        statuses = ["wait_pay", "wait_send", "wait_receive", "complete", "close"]
        order_statuses = [order_status, order_status]
        if order_status == "all":
            import random
            order_statuses = [statuses[random.randint(0, 4)], statuses[random.randint(0, 4)]]
        res = [
            {
                "code": "123465789542525",  # 订单编码
                "name": "G-STEP冬季卫衣",
                "thumbnails": "img/thumbnails2.jpg",  # 小缩略图
                "properties": [
                    {
                        "name": "颜色",
                        "type": "黑色"
                    },
                    {
                        "name": "大小",
                        "type": "S"
                    },
                    {
                        "name": "其他",
                        "type": "t1"
                    },
                ],
                "price": "490.5",
                "count": 1,  # 商品个数
                "time": "2019-12-12 02:23:14",  # 该订单变更为当前状态的时间
                "address_id": "3453",  # 物流信息id可以根据该id获取物流详细细信息
                "order_status": order_statuses[0],  # 订单状态
                "presell_count": 100,  # 总共想预售的数量
                "sold_count": 68,  # 已经卖的数量
                "satisfy_count": 20,  # 满多少件发货
                "seed_id": "aaaaaaaaa"  # 商品id,由系统后台确定且唯一
            },
            {
                "code": "223465789543242",
                "name": "G-STEP门票",
                "thumbnails": "img/thumbnails2.jpg",
                "properties": [
                    {
                        "name": "排",
                        "type": "4"
                    },
                    {
                        "name": "列",
                        "type": "2"
                    },
                    {
                        "name": "区域",
                        "type": "1"
                    },
                ],
                "price": "50",
                "count": 5,  # 商品数量
                "time": "2019-12-12 02:23:14",  # 该订单变更为当前状态的时间
                "address_id": "3432",  # 物流信息id可以根据该id获取物流详细细信息
                "order_status": order_statuses[1],  # wait_pay(代付款)、wait_send(待发货)、wait_receive(待收货)、已完成
                "presell_count": 100,  # 总共想预售的数量
                "sold_count": 68,  # 已经卖的数量
                "satisfy_count": 20,  # 满多少件发货
                "seed_id": "aaaaaaaaa"  # 商品id,由系统后台确定且唯一
            }
        ]
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({"reason": "", "res": res}))


class AddressesHandler(BaseHandler):
    def get(self):
        res = [
            {
                "name": "范晓宇",
                "country": "中国",
                "province": "北京市",
                "region": "朝阳区",
                "address": "酒仙桥6号院电子国际总部",
                "phone": "13552266949",
                "default": 1,  # 默认收获地址
                "address_id": 1,  # 地址id,整个系统唯一
            },
            {
                "name": "李颖",
                "country": "中国",  # 国家
                "province": "北京市",  # 省(直辖市)
                "region": "朝阳区",  # 县(区)
                "address": "酒仙桥6号院电子国际总部",  # 具体地址
                "phone": "18966677772",
                "default": 0,  # 非默认收获地址
                "address_id": 2,  # 地址id,整个系统唯一
            }
        ]
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({"reason": "", "res": res}))


class AddressGetHandler(BaseHandler):
    def post(self):
        # 期待接收的参数
        # ["address_id1", "address_id2"] # 列表
        res = [
            {
                "name": "范晓宇",
                "country": "中国",
                "province": "北京市",
                "region": "朝阳区",
                "address": "酒仙桥6号院电子国际总部",
                "phone": "13552266949",
                "default": 1,  # 默认收获地址
                "address_id": 1,  # 地址id,整个系统唯一
            },
            {
                "name": "李颖",
                "country": "中国",  # 国家
                "province": "北京市",  # 省(直辖市)
                "region": "朝阳区",  # 县(区)
                "address": "酒仙桥6号院电子国际总部",  # 具体地址
                "phone": "18966677772",
                "default": 0,  # 非默认收获地址
                "address_id": 2,  # 地址id,整个系统唯一
            }
        ]
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({"reason": "", "res": res}))


class AddressDDLHandler(BaseHandler):
    def post(self):
        ddl = self.get_argument("ddl")
        # 期望接收到的post_json
        # 修改地址时:
        # {
        #     "ddl":"change"   #值必须是change
        #     "name": "李颖",
        #     "country": "中国",  # 国家
        #     "province": "北京市",  # 省(直辖市)
        #     "region": "朝阳区",  # 县(区)
        #     "address": "酒仙桥6号院电子国际总部",  # 具体地址
        #     "phone": "18966677772",
        #     "default": 0,  # 非默认收获地址
        #     "address_id": 2,  # 地址id,整个系统唯一
        # }
        # 增加地址时
        # {
        #     "ddl":"insert"   #值必须是insert
        #     "name": "李颖",
        #     "country": "中国",  # 国家
        #     "province": "北京市",  # 省(直辖市)
        #     "region": "朝阳区",  # 县(区)
        #     "address": "酒仙桥6号院电子国际总部",  # 具体地址
        #     "phone": "18966677772",
        #     "default": 0,  # 非默认收获地址
        # }
        # 删除地址时
        # {
        #     "ddl":"delete"   #值必须是delete
        #     "address_id": 1 # 地址id,整个系统唯一
        # }
        res = {}
        if ddl == "insert":
            name = self.get_argument("name")
            country = self.get_argument("country")
            province = self.get_argument("province")
            region = self.get_argument("region")
            address = self.get_argument("address")
            phone = self.get_argument("phone")
            default = self.get_argument("phone")
        elif ddl == "change":
            address_id = self.get_argument("address_id")
            name = self.get_argument("name")
            country = self.get_argument("country")
            province = self.get_argument("province")
            region = self.get_argument("region")
            address = self.get_argument("address")
            phone = self.get_argument("phone")
            default = self.get_argument("phone")
            if ddl == "insert":
                pass
            elif ddl == "change":
                pass
        else:
            id = self.get_argument("id")
            pass
        res = {"address_id": "sadfasdf"}
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({"reason": "", "res": res}))


class PayHandler(BaseHandler):
    # 期待接收的参数
    # {"code:"dfdfdf"} #订单号
    def post(self):
        res = {}
        self.write(json.dumps({"reason": "", "res": res}))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        # (\d+)表示数字，例如想请求商品主页接口CommodityIndexHandler，url:http://test.preseller.gsteps.cn/api/commodity/324234242423,
        handlers=[
            (r"/api/commodity/(\d+)", CommodityIndexHandler),  # 商品主页，在微信中发布商品信息用到展示商品信息接口
            (r"/api/recomends/(\d+)", RecommendHandler),  # 靠谱推荐接口
            (r"/api/publisher/(\d+)", PublisherHandler),  # 发布方信息接口
            (r"/api/purchase/detail/(\d+)", PurchaseDetailHandler),  # 商品详情
            (r"/api/cart/add/(\d+)", CartAddHandler),  # 加入购物车
            (r"/api/cart/delete/", CartDeleteHandler),  # 从购物车中删除
            (r"/api/cart/modify/", CartModifyHandler),  # 修改购物车中商品信息
            (r"/api/cart/detail/", CartDetailHandler),  # 根据购物车id列表获取购物车详情
            (r"/api/cart/all/", CartAllHandler),  # 根据购物车id列表获取购物车详情
            (r"/api/order/add", OrderAddHandler),  # 下订单，需要提供购物车列表和物流id
            # 用户商品信息接口，根据提供不同的状态，返回不同状态的订单 wait_pay(代付款)、wait_send(待发货)、wait_receive(待收货)、complete（已完成）
            (r"/api/order/status", OrderStatusHandler),  # 根据订单状态获取订单详情
            (r"/api/order/get", OrderGetHandler),  # 根据订单编号列表获取订单详情
            (r"/api/order/delete", OrderDeleteHandler),  # 根据订单编号列表删除订单
            (r"/api/addresses/", AddressesHandler),  # 获取用户地址信息接口
            (r"/api/address/ddl", AddressDDLHandler),  # 对用户地址进行增删改的接口
            (r"/api/address/get", AddressGetHandler),  # 根据address_id列表获取物流信息
            (r"/api/pay", PayHandler),  # 支付
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


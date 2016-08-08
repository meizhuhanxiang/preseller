#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler


class PublisherHandler(BaseHandler):
    def get(self, seed_id):
        # a = self.get_argument('noun1')
        res = {
            'navigation_img': '/img/navigation_img.jpg',
            'brief_introduction': '我们的设计师都来自各个互联网公司的顶尖成员，都热爱hip-hop这个文化，我们以hip-hop为主题进行设计，以嘻哈的态度表达我们的生活，希望你能同感',
            'guarantee': '我们与广东的几个不错的加工厂有长期合作，她们代工的产品，在淘宝上一般都在200元左右，我们试穿了很长时间，认为比较靠谱，如果你认为不好，只要能指出问题，我们包退哦',
            'activity_photos': [
                '/img/activity_photo1.jpg',
                '/img/activity_photo2.jpg',
                '/img/activity_photo3.jpg',
            ]
        }
        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write(json.dumps({'reason': '', 'res': res}))


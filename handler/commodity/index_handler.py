#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler, handler
from model import ModelConfig
from model import CommodityModel
from model import PublisherModel
from model import RecommendModel
from model import UserModel
from model import OrderModel


class IndexHandler(BaseHandler):
    @handler
    def post(self):
        commodity_id = self.get_json_argument('commodity_id')

        commodity_model = self.model_config.first(CommodityModel, id=commodity_id)  # type: CommodityModel
        publisher_model = self.model_config.first(PublisherModel,
                                                  id=commodity_model.publisher_id)  # type: PublisherModel
        recommend_models = self.model_config.all(RecommendModel,
                                                 commodity_id=commodity_model.id)  # type: RecommendModel
        order_models = self.model_config.all(OrderModel, user_id=1, status=OrderModel.STATUS_CART)
        count = 0
        for order_model in order_models: #type:OrderModel
            count += order_model.count
        res = {
            'commodity_id': commodity_id,  # 商品id
            'title': commodity_model.title,
            'brief': commodity_model.brief,
            'navigation': '/%s/preseller/img/commodity/%s/navigation.png' % (
                self.get_inner_static_path(), commodity_id),
            'presell_count': commodity_model.presell_count,  # 总共想预售的数量
            'sold_count': commodity_model.sold_count,  # 已经卖的数量
            'satisfy_count': commodity_model.satisfy_count,  # 满多少件发货
            'logo': '%s/preseller/img/publisher/%s/logo.png' % (self.get_inner_static_path(), commodity_id),
            'publisher_name': publisher_model.name,
            'cart_count': count,  # 购物袋中商品的数量
            'detail': ['%s/preseller/img/commodity/%s/detail/%s.jpg' % (self.get_inner_static_path(), commodity_id, i)
                       for i in xrange(commodity_model.detail_img_count)]
        }
        recommends = []
        for recommend_model in recommend_models:  # type: RecommendModel
            user_model = self.model_config.first(UserModel, id=recommend_model.user_id, is_v=1)  # type: UserModel
            if user_model:
                recommends.append({
                    'profile': user_model.profile,
                    'name': user_model.name,
                    'job': user_model.job,
                    'is_v': user_model.is_v,
                    'content': recommend_model.content
                })
        res['recommends'] = recommends
        return res

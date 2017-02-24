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
from model import DetailModel
from utils.exception import *


class RuleHandler(BaseHandler):
    @handler
    def post(self):
        commodity_id = self.get_json_argument('commodity_id')

        commodity_model = self.model_config.first(CommodityModel, id=commodity_id)  # type:CommodityModel
        if not commodity_model:
            raise ServerError(ServerError.ARGS_ILLEGAL)
        detail_models = self.model_config.all(DetailModel, fk_id=commodity_model.id,
                                              fk_type=DetailModel.FK_TYPE_RULE)
        res = []
        for detail_model in detail_models:  # type:DetailModel
            res.append({
                'title': detail_model.title,
                'text': detail_model.text,
                'image': '%s/preseller/img/commodity/%s/rule/%s' % (
                    self.get_inner_static_path(), commodity_model.id,
                    detail_model.image) if detail_model.image else None
            })
        return res

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
from utils.exception import *


class RuleHandler(BaseHandler):
    @handler
    def post(self):
        commodity_id = self.get_json_argument('commodity_id')

        commodity_model = self.model_config.first(CommodityModel, id=commodity_id)
        if not commodity_model:
            raise ServerError(ServerError.ARGS_ILLEGAL)
        res = {
            'detail': '/%s/preseller/img/commodity/%s/rule.jpg' % (self.get_inner_static_path(), commodity_id)
        }
        return res

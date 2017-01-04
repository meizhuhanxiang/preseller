#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from utils.logger import runtime_logger
from utils.code import *
from handler.base.base_handler import BaseHandler


class RecommendHandler(BaseHandler):
    def post(self):
        args = self.get_need_args(['purchase_id'])
        if self.code != SUCCESS:
            self.write_res({})
            return
        purchase_id = args['purchase_id']
        purchase = Purchase()
        res = purchase.recommend(purchase_id)
        self.write_res(res)

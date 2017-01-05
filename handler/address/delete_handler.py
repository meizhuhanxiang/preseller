#!/usr/bin/python
# -*- coding: utf-8 -*-
from handler.base.base_handler import BaseHandler, handler
from model import AddressModel
from model import ModelConfig


class DeleteHandler(BaseHandler):
    @handler
    def post(self):
        address_id = self.get_json_argument('address_id')
        model_config = ModelConfig()
        address_model = model_config.first(AddressModel, user_id=1, id=address_id)
        if address_model:
            model_config.delete(address_model)

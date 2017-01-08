#!/usr/bin/python
# -*- coding: utf-8 -*-
from handler.base.base_handler import BaseHandler, handler
from model import AddressModel
from model import ModelConfig
from utils.exception import *


class DefaultHandler(BaseHandler):
    @handler
    def post(self):
        address_id = self.get_json_argument('address_id')
        address_model = self.model_config.first(AddressModel, user_id=1, id=address_id)  # type:AddressModel
        if not address_model:
            raise ServerError(ServerError.ADDRESS_ID_NO_EXIST, args=address_id)
        address_models = self.model_config.all(AddressModel, default=True)
        for model in address_models:  # type:AddressModel
            model.default = False
        address_model.default = True
        self.model_config.commit()

#!/usr/bin/python
# -*- coding: utf-8 -*-
from handler.base.base_handler import BaseHandler, handler
from model import AddressModel
from model import ModelConfig


class DeleteHandler(BaseHandler):
    @handler
    def post(self):
        address_id = self.get_json_argument('address_id')

        address_model = self.model_config.first(AddressModel, user_id=1, id=address_id)  # type:AddressModel
        default = address_model.default
        if address_model:
            self.model_config.delete(address_model)
        if default:
            address_model = self.model_config.first(AddressModel, user_id=1)  # type:AddressModel
            address_model.default = True
            self.model_config.commit()
        else:
            address_model = self.model_config.first(AddressModel, user_id=1, default=True)  # type:AddressModel
        res = {
            'default_address_id': address_model.id
        }
        return res

#!/usr/bin/python
# -*- coding: utf-8 -*-
from handler.base.base_handler import BaseHandler, handler
from model import AddressModel
from model import ModelConfig


class ModifyHandler(BaseHandler):
    @handler
    def post(self):
        address_id = self.get_json_argument('address_id')
        name = self.get_json_argument('name', '', allow_null=True)
        country = self.get_json_argument('country')
        province = self.get_json_argument('province')
        municipality = self.get_json_argument('municipality')
        region = self.get_json_argument('region')
        address = self.get_json_argument('address')
        phone = self.get_json_argument('phone')
        default = self.get_json_argument('default')

        model_config = ModelConfig()
        if True == default:
            address_models = model_config.all(AddressModel, default=True)
            for address_model in address_models:  # type:AddressModel
                address_model.default = False
        address_model = model_config.first(AddressModel, user_id=1, id=address_id)  # type:AddressModel
        address_model.name = name
        address_model.country = country
        address_model.province = province
        address_model.municipality = municipality
        address_model.region = region
        address_model.address = address
        address_model.phone = phone
        address_model.default = default
        model_config.flush()
        model_config.commit()

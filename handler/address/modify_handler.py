#!/usr/bin/python
# -*- coding: utf-8 -*-
from handler.base.base_handler import BaseHandler, handler
from model import AddressModel
from model import ModelConfig
from utils.exception import *


class ModifyHandler(BaseHandler):
    @handler
    def post(self):
        address_id = self.get_json_argument('address_id')
        name = self.get_json_argument('name')
        country = self.get_json_argument('country')
        province = self.get_json_argument('province')
        municipality = self.get_json_argument('municipality')
        region = self.get_json_argument('region')
        address = self.get_json_argument('address')
        phone = self.get_json_argument('phone')
        address_model = self.model_config.first(AddressModel, user_id=1, id=address_id)  # type:AddressModel
        if not address_model:
            raise ServerError(ServerError.ADDRESS_ID_NO_EXIST, args=address_id)
        # if True == default:
        #     address_models = self.model_config.all(AddressModel, default=True)
        #     for address_model in address_models:  # type:AddressModel
        #         address_model.default = False
        address_model = self.model_config.first(AddressModel, user_id=1, id=address_id)  # type:AddressModel
        address_model.name = name
        address_model.country = country
        address_model.province = province
        address_model.municipality = municipality
        address_model.region = region
        address_model.address = address
        address_model.phone = phone

        self.model_config.commit()

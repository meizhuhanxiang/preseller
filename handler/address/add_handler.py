#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler, handler
from model import AddressModel
from model import ModelConfig


class AddHandler(BaseHandler):
    @handler
    def post(self):
        name = self.get_json_argument('name')
        country = self.get_json_argument('country')
        province = self.get_json_argument('province')
        municipality = self.get_json_argument('municipality')
        region = self.get_json_argument('region')
        address = self.get_json_argument('address')
        phone = self.get_json_argument('phone')
        default = self.get_json_argument('default')
        if self.model_config.count(AddressModel):
            if True == default:
                address_models = self.model_config.all(AddressModel, default=True)
                for address_model in address_models:  # type:AddressModel
                    address_model.default = False

                self.model_config.commit()
        else:
            default = True
        address_model = AddressModel(user_id=1, name=name, country=country, province=province,
                                     municipality=municipality, region=region, address=address,
                                     phone=phone, default=default)
        self.model_config.add(address_model)
        res = {
            'address_id': address_model.id
        }
        return res

#!/usr/bin/python
# -*- coding: utf-8 -*-
from handler.base.base_handler import BaseHandler, handler
from model import AddressModel
from model import ModelConfig


class GetHandler(BaseHandler):
    @handler
    def post(self):
        address_ids = self.get_json_argument("address_ids", [], allow_null=True)
        model_config = ModelConfig()

        if address_ids:
            address_models = model_config.filter_all(AddressModel, user_id=1,
                                                     filters=AddressModel.id.in_(tuple(address_ids)))
        else:
            address_models = model_config.all(AddressModel, user_id=1)
        res = []
        for address_model in address_models:  # type:AddressModel
            address = {
                "id": address_model.id,
                "name": address_model.name,
                "country": address_model.country,
                "province": address_model.province,
                "municipality": address_model.municipality,
                "region": address_model.region,
                "address": address_model.address,
                "phone": address_model.phone,
                "default": address_model.default
            }
            res.append(address)
        return res

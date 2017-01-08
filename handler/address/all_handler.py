#!/usr/bin/python
# -*- coding: utf-8 -*-
from handler.base.base_handler import BaseHandler, handler
from model import AddressModel
from model import ModelConfig


class AllHandler(BaseHandler):
    @handler
    def post(self):
        address_ids = self.get_json_argument("address_ids", [], allow_null=True)
        model_config = ModelConfig()
        res = {
            "default": None,
            "other": []
        }
        address_models = model_config.all(AddressModel, user_id=1)
        for address_model in address_models:  # type:AddressModel
            address = {
                "id": address_model.id,
                "name": address_model.name,
                "country": address_model.country,
                "province": address_model.province,
                "municipality": address_model.municipality,
                "region": address_model.region,
                "address":address_model.address,
                "phone": address_model.phone,
                "default": address_model.default
            }
            if address_model.default:
                if res["default"]:
                    address_model.default = False
                    res['default'] = False
                    res['other'].append(address)
                else:
                    res["default"] = address
            else:
                res['other'].append(address)
        model_config.flush()
        model_config.commit()
        return res

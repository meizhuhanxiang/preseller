#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from handler.base.base_handler import BaseHandler, handler
from model import CityModel
from model import ModelConfig


class City3levelHandler(BaseHandler):
    @handler
    def post(self):
        model_id = self.get_json_argument('id', None, allow_null=True)

        res = []
        if not model_id:
            city_models = self.model_config.all(CityModel, level=0)
        else:
            city_model = self.model_config.first(CityModel, id=model_id)  # type:CityModel
            city_models = self.model_config.all(CityModel, parent_id=city_model.id)
        for city_model in city_models:  # type:CityModel
            res.append({
                'id': city_model.id,
                'level': city_model.level,
                'first_letter': city_model.first_letter,
                'code': city_model.code,
                'name': city_model.name
            })
        return res

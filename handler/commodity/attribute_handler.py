#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from model import CommodityModel
from model import OptionModel
from model.commodity import CommodityModel
from model import AttributeModel
from model import ModelConfig
from utils.exception import ServerError

from handler.base.base_handler import BaseHandler, handler


class AttributeHandler(BaseHandler):
    @handler
    def post(self):
        commodity_id = self.get_json_argument('commodity_id')
        selected_option_ids = self.get_json_argument('selected_option_ids', default=[], allow_null=True)
        count = self.get_json_argument('count', default=1, allow_null=True)
        model_config = ModelConfig()
        commodity_model = model_config.first(CommodityModel, id=commodity_id)  # type: CommodityModel
        attribute_models = model_config.all(AttributeModel, commodity_id=commodity_id)
        selected_option_models = model_config.filter_all(OptionModel,
                                                         OptionModel.id.in_(tuple(selected_option_ids)))
        selected_attr_names = []
        for selected_option_model in selected_option_models:  # type:OptionModel
            attribute_model = model_config.first(AttributeModel,
                                                 id=selected_option_model.attr_id)  # type:AttributeModel
            selected_attr_names.append(attribute_model.attr_name)
        res = {
            'commodity_id': commodity_id,
            'title': commodity_model.title,
            'count': count,
            'base_price': commodity_model.base_price
        }
        attributes = {}
        for attribute_model in attribute_models:  # type: AttributeModel
            attributes[attribute_model.attr_name] = {
                'attr_name': attribute_model.attr_name,
                'cn_attr_name': attribute_model.cn_attr_name,
                'index': attribute_model.index,
                'options': []
            }
            option_models = model_config.all(OptionModel, attr_id=attribute_model.id)
            options = []
            for option_model in option_models:  # type:OptionModel
                option = {
                    'option_id': option_model.id,
                    'option_name': option_model.option_name,
                    'cn_option_name': option_model.cn_option_name,
                    'weight': option_model.weight,
                    'default': option_model.default,
                    'index': option_model.index,
                    'select': False
                }
                options.append(option)
            attributes[attribute_model.attr_name]['options'] = options

        select_option = {}
        if len(selected_attr_names) == 0:
            for attr_name, options in attributes.items():
                has_default = False
                for option in options['options']:
                    if option['default']:
                        has_default = True
                        select_option[option['option_id']] = option['weight']
                        option['select'] = True
                        break
                if not has_default:
                    first_option = options['options'][0]
                    select_option[first_option['option_id']] = first_option['weight']
                    first_option['select'] = True
        else:
            attribute_names = attributes.keys()
            if (len(set(selected_attr_names)) != len(selected_attr_names) or
                        set(selected_attr_names) != set(attribute_names)):
                raise ServerError(ServerError.ARGS_ILLEGAL)
            for attr_name, options in attributes.items():
                has_select = False
                for option in options['options']:
                    if option['option_id'] in selected_option_ids:
                        has_select = True
                        select_option[option['option_id']] = option['weight']
                        option['select'] = True
                        break
                if not has_select:
                    raise ServerError(ServerError.ARGS_ILLEGAL)
                options['options'] = sorted(options['options'], key=lambda option: option['index'])
        attributes = [v for k, v in attributes.items()]
        attributes = sorted(attributes, key=lambda attribute: attribute['index'])
        selected_first_option = ''
        for option in attributes[0]['options']:
            if option['select']:
                selected_first_option = option['option_name']

        price = commodity_model.base_price
        for option_id, weight in select_option.items():
            price += weight
        res['sample_img'] = '/%s/preseller/img/commodity/%s/attribute/%s.jpg' % (
            self.get_inner_static_path(), commodity_id, selected_first_option)
        res['price'] = price * count
        res['attributes'] = attributes
        model_config.flush()
        model_config.commit()
        return res

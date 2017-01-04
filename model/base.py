#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import TypeDecorator
from sqlalchemy import types
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import BOOLEAN
from sqlalchemy import text, Text
from sqlalchemy import DateTime

__author__ = 'guoguangchuan'

__all__ = ['List', 'Dict', 'Base']


class Json(TypeDecorator):
    @property
    def python_type(self):
        return self._type

    impl = Text
    _null = None
    _type = object

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_literal_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            value = self._null
        return value


class List(Json):
    _null = []
    _type = list


class Dict(Json):
    _null = {}
    _type = dict


MutableDict.associate_with(Dict)

Base = declarative_base()

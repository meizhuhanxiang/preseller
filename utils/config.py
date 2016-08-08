#!/usr/bin/python
# encoding:utf-8

from ConfigParser import RawConfigParser


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class Configuration:
    def __init__(self):
        self._config_file = 'conf/app.ini'
        self._load()

    def _load(self):
        self._config = RawConfigParser()
        self._config.read(self._config_file)

    def get(self, sect, opt):
        return self._config.get(sect, opt)

    def get_section(self, section):
        if not self._config.has_section(section):
            return {}
        items = self._config.items(section)
        return dict(items)


def get(sect, opt):
    return Configuration().get(sect, opt)


def get_section(sect):
    return Configuration().get_section(sect)

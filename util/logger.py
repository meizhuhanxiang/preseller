#!/usr/bin/python
# encoding:utf-8

import os
import sys
import logging
import logging.config

import util.config

this_path = os.path.dirname(os.path.abspath(sys.argv[0]))
if not this_path:
    this_path = '.'

log_path = util.config.get('global', 'log_path')
if not log_path:
    log_path = os.path.join(this_path, "logs")

conf_file = os.path.join(os.getenv('CONF'), 'logging.conf')

logging.config.fileConfig(conf_file, defaults={'log_path': log_path})


def api_logger():
    return logging.getLogger('service')


def runtime_logger():
    return logging.getLogger('runtime')


def task_logger():
    return logging.getLogger('task')
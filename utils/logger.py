#!/usr/bin/python
# encoding:utf-8


import os
import logging
import logging.config

FORCE_ABSOLUTE_PATH = False

conf_file = os.path.join(os.getcwd(), 'conf', 'logger.ini')
log_path = os.path.join(os.getcwd(), 'log')

logging.config.fileConfig(conf_file, defaults={'log_path': log_path})


def api_logger():
    return logging.getLogger('service')


def runtime_logger():
    return logging.getLogger('runtime')


def task_logger():
    return logging.getLogger('task')

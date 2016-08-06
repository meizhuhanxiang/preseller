# -*- coding: utf-8 -*-
__author__ = 'guoguangchuan'


from tools.global_conf import *


def get_remain_cheer_num(cheer_num):
    remain_cheer_num = SATISFY_CHEER_NUM - cheer_num
    if remain_cheer_num < 0:
        remain_cheer_num = 0
    return remain_cheer_num

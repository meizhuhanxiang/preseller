#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
基础异常类, 为了更好的管理客户端异常状态, 客户端禁止抛出其他异常
"""
__author__ = 'guoguangchuan'


class BaseError(Exception):
    BASE_CODE = 0
    message_zh = ''

    def __init__(self, status, **kwargs):
        self.status_code = int(status[0])
        try:
            self.message = status[1].format(**kwargs)
            self.message_zh = status[2].format(**kwargs)
        except KeyError, e:
            raise Exception('Arg missing for exception: %s' % e)

    def split(self):
        return self.status_code + self.BASE_CODE, '{msg}'.format(msg=(self.message_zh or self.message))

    def __repr__(self):
        return u'StatusCode: %s, Message: %s' % (self.BASE_CODE + self.status_code, self.message)

    def __str__(self):
        return self.__repr__()


class LocalServerError(BaseError):
    BASE_CODE = 50000
    ARGS_MISSING = (1, '{args} are required.', '缺少参数{args}')


class DatabaseError(BaseError):
    BASE_CODE = 10000
    DATABASE_COMMIT_ERROR = (1, 'Database commit error:{args}', '提交数据库发生错误, 已回滚请重试, 错误信息:{args}')


class NetworkError(BaseError):
    BASE_CODE = 20000


class ServerError(BaseError):
    BASE_CODE = 30000
    ARGS_MISSING = (1, '{args} are required.', '缺少参数{args}')
    ARGS_ILLEGAL = (2, 'arguments illegal or not complete', '参数不合法或者不完整')
    ADDRESS_ID_NO_EXIST = (3, 'address_id: {args} is not exist', '地址id:{args} 不存在')
    ORDER_ID_ILLEGEL = (4, 'order_id: {args} is illegel', '订单id:{args} 不合法')
    USER_NO_LOGIN = (5, 'user is not logined', '用户未登陆')
    CART_ADD_IDS_NOT_MATCH = (6, 'cart add ids is not match', '添加购物车提供的id不合法')
    ORDER_STATUS_ILLEGAL = (6, 'order status {args} is not illegal', '订单查询状态参数"{args}"不存在或不合法')


class SyncError(BaseError):
    BASE_CODE = 40000
    ARG_MISSING = (1, 'Arg missing: {arg}', '缺失参数: {arg}')


if __name__ == '__main__':
    raise SyncError(SyncError.UPDATE_IS_STARTING)

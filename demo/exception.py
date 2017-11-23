#!/usr/bin/env python
# -*- coding: utf-8 -*-

import repr
from base import Message


class SQLException(Exception):
    """
    数据库异常
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NotFoundException(Exception):
    """
    查询无记录
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InitializException(Exception):
    """
    实例化错误
    """

    def __init__(self, value):
        self.value = value


class UnknownTypeException(Exception):
    """
    非法标签类型
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class IllegalArgumentException(Exception):
    """
    参数错误
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UserDisableException(Exception):
    """
    用户禁用
    """

    def __init__(self, value=Message.USER_DISABLE_EXCEPTION):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UserInvlidException(Exception):
    """
    用户失效
    """

    def __init__(self, value=Message.USER_INVALID_EXCEPTION):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RemoteException(Exception):
    """
    远程请求异常
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RoleDisableException(Exception):
    """
    角色禁用
    """

    def __init__(self, value=Message.ROLE_DISABLE_EXCEPTION):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SmsCodeException(Exception):
    """
    短信验证码异常
    """

    def __init__(self, value=Message.SMS_CODE_EXPIRE):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UserExistsException(Exception):
    """
    用户已存在异常
    """

    def __init__(self, value=Message.USER_EXISTS_EXCEPTION):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SMSToManyException(Exception):
    """
    用户已存在异常
    """

    def __init__(self, value=Message.SMS_TOO_MANY_EXCEPTION):
        self.value = value

    def __str__(self):
        return repr(self.value)

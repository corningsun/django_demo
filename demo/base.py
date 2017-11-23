#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from django.http import HttpResponse


def obj2json(obj):
    return json.dumps(obj, ensure_ascii=False, cls=ObjJsonEncoder, encoding='utf-8', indent=1)


def object2dict(obj):
    # 基本数据类型，直接返回
    if not hasattr(obj, '__dict__'):
        return obj
    rst = {}
    for k, v in obj.__dict__.items():
        if k.startswith('-'):
            continue
        if isinstance(v, list):
            ele = [object2dict(item) for item in v]
        else:
            ele = object2dict(v)
        rst[k] = ele
    return rst


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = obj2json(data)
        kwargs['content_type'] = 'application/json;charset=UTF-8;'
        super(JSONResponse, self).__init__(content, **kwargs)


class ResponseBody:
    def __init__(self, info, code, message):
        self.info = info
        self.code = code
        self.message = message


class ObjJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        return object2dict(obj)


class Code:
    SUCCESS = 200
    ERROR = 500
    NOT_FOUND = 250
    TOKEN = 300
    ARGUMENT = 210
    UNKNOWN_TYPE = 220


class Message:
    SUCCESS = "success"
    ERROR = "error"
    NOT_FOUND = "not found"
    NO_TOKEN = '请求不合法，不包含TOKEN信息!'
    ILLEGAL_TOKEN = '登录失效，请重新登录!'
    ILLEGAL_USER = '用户不存在!'
    EXPIRE_TOKEN = '用户token超时'
    NOT_FOUND_EXCEPTION = '暂无记录!'
    ID_NOT_FOUND_EXCEPTION = '%s=%s, 查无此记录!'
    USER_NOT_FOUND_EXCEPTION = '用户名或密码不正确!'
    ROLE_NOT_FOUND_EXCEPTION = '角色不存在!'
    INITIALIZ_EXCEPTION = '实例化出错!'
    NOT_ACCESSIBLE = '没有权限!'
    UNKNOWN_TYPE = 'type:%s, 查无此标签!'
    USER_DISABLE_EXCEPTION = '您的账号登录已被禁用，若有疑问请联系客服！'
    USER_INVALID_EXCEPTION = '您的账号登录已失效，若有疑问请联系客服！'
    ROLE_DISABLE_EXCEPTION = '此账号对应的角色已被禁用，若有疑问请联系客服！'
    OLD_PASSWORD_ERROR = '原密码错误！'
    NEW_PASSWORD_SAME = '新密码不能和原密码相同！'
    USER_NOT_LOGIN = '用户未登录！'
    SMS_CODE_NOT_EXISTS = '请先获取短信验证码！'
    SMS_CODE_EXPIRE = '验证码已过期，请重新获取！'
    SMS_CODE_ERROR = '请输入正确的验证码！'
    USER_EXISTS_EXCEPTION = '该手机号已存在！无法重复绑定'
    BIND_MOBILE_SUCCESS = '手机修改绑定成功！'
    MODIFY_PASSWORD_SUCCESS = '密码修改成功！'
    SMS_TOO_MANY_EXCEPTION = '您今天发送过于频繁，请改日再试！'
    USER_EXISTS_YES = 'YES'
    USER_EXISTS_NO = 'NO'
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

from demo.base import Message, CommonStatus
from demo.exception import NotFoundException, UserDisableException
from demo.signature import Signature


class UserService(object):
    DEMO_USER = {
        "id": 1,
        "name": "demo",
        "status": 1,
        "role_id": 1
    }

    @staticmethod
    def queryById(user_id):
        # TODO
        return UserService.DEMO_USER

    @staticmethod
    def check_user_role(user, req_path):
        # TODO 校验用户权限
        return True

    @staticmethod
    def queryUser(username, password):
        if username == 'demo' and password == 'demo':
            return UserService.DEMO_USER
        else:
            raise NotFoundException(Message.USER_NOT_FOUND_EXCEPTION)


class LoginService(object):
    @staticmethod
    def login(username, password, remember):
        user = UserService.queryUser(username, password)
        """
        是否禁用
        """
        if user['status'] == CommonStatus.DISABLE:
            raise UserDisableException()

        token = Signature.encodeJwt(user['id'], user['role_id'], remember)
        return {'token': token, 'userId': user['id'], 'username': user['name']}


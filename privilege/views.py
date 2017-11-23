# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from demo.base import ResponseBody, Code, Message, JSONResponse
from demo.exception import NotFoundException, UserInvlidException, RoleDisableException
from demo.exception import UserDisableException
from privilege.service import LoginService

logger = logging.getLogger('django')


class Login(APIView):
    def post(self, request):
        """
        用户登录
        ---
            :param username: 用户名
            :param password: 密码
            :param remember: 是否缓存，true／false
        """
        try:
            data = request.data

            remember = data.get('remember')
            if remember is None:
                remember = 'false'

            info = LoginService.login(data['username'], data['password'], remember)
            responseBody = ResponseBody(info, Code.SUCCESS, Message.SUCCESS)
        except (NotFoundException, UserDisableException, UserInvlidException, RoleDisableException), e:
            logger.exception(e.value)
            responseBody = ResponseBody({}, Code.TOKEN, e.value)
        except Exception, e:
            logger.exception(e)
            responseBody = ResponseBody({}, Code.ERROR, Message.ERROR)

        return JSONResponse(responseBody)

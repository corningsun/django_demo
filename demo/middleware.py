#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin

from privilege.service import UserService, OperationService
from utils import *
from base import *

from demo.utils import DateUtils
from exception import *
import logging
from signature import Signature

logger = logging.getLogger('django')


class TokenMiddleware(MiddlewareMixin):
    """
    token拦截器
    """
    header_key = 'HTTP_AUTHORIZATION'

    def expires(self, iatstr, remember):
        """
        判断token是否过期
        """
        iat = DateUtils.parse(iatstr)
        now = DateUtils.now()
        return DateUtils.timeDiff(now, iat) > (
            Constant.EXPIRES_TIME if remember == 'true' else Constant.DEFAULT_EXPIRES_TIME)

    def parse_header(self, jwt):
        return Signature.decodeJwt(jwt)

    def process_request(self, request):
        try:
            req_path = request.path
            if request.META.has_key(self.header_key):
                jwt = request.META[self.header_key]

                payload = self.parse_header(jwt)

                if payload is None:
                    if not OperationService.is_guest_operation(req_path):
                        return JSONResponse(ResponseBody({}, Code.ERROR, Message.ILLEGAL_TOKEN))
                    else:
                        return

                user = UserService.queryById(payload['from_user'])
                if not user:
                    return JSONResponse(ResponseBody({}, Code.ERROR, Message.ILLEGAL_USER))

                if self.expires(payload['iat'], payload['remember']):
                    return JSONResponse(ResponseBody({}, Code.ERROR, Message.EXPIRE_TOKEN))

                UserManage.thread_local.user = user
            else:
                if OperationService.is_guest_operation(req_path):
                    pass
                else:
                    return JSONResponse(ResponseBody({}, Code.TOKEN, Message.NO_TOKEN))
        except InitializException, e:
            logger.exception(e.value)
            return JSONResponse(ResponseBody({}, Code.ERROR, e.value))
        except Exception, e:
            logger.exception(e)
            return JSONResponse(ResponseBody({}, Code.ERROR, Message.ERROR))


class PrivilegeMiddleware(MiddlewareMixin):
    """
    权限拦截器
    """

    def process_request(self, request):
        try:
            req_path = request.path

            if OperationService.is_guest_operation(req_path):
                return

            user = UserManage.get_current_user()
            if not UserService.check_user_role(user, req_path):
                return JSONResponse(ResponseBody({}, Code.ERROR, Message.NOT_ACCESSIBLE))
        except Exception, e:
            logger.exception(e)
            JSONResponse(ResponseBody({}, Code.ERROR, Message.ERROR))
        return None

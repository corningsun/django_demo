# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from demo.base import *
from demo.exception import NotFoundException

logger = logging.getLogger('django')


class Hello(APIView):
    def get(self, request, name):
        try:
            info = "Hello %s" % name
            responseBody = ResponseBody(info, Code.SUCCESS, Message.SUCCESS)
        except NotFoundException, e:
            logger.exception(e.value)
            responseBody = ResponseBody({}, Code.NOT_FOUND, e.value)
        except Exception, e:
            logger.exception(e)
            responseBody = ResponseBody({}, Code.ERROR, Message.ERROR)
        return JSONResponse(responseBody)
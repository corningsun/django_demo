#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itsdangerous import JSONWebSignatureSerializer
from itsdangerous import BadData, BadSignature
from utils import DateUtils


class Signature():
    '''
    用户签名
    '''
    salt = 'demo'

    s = JSONWebSignatureSerializer(salt)

    @staticmethod
    def encodeJwt(id, role, remember):
        '''
        生成jwt
        '''
        payload = {
            'iat': DateUtils.format(DateUtils.now()),
            'from_user': id,
            'role': role,
            'remember': remember
        }
        return Signature.s.dumps(payload, Signature.salt)

    @staticmethod
    def decodeJwt(jwt):
        '''
        加载jwt
        '''
        decoded_payload = None
        try:
            decoded_payload = Signature.s.loads(jwt)
        except BadSignature, e:
            encoded_payload = e.payload
            if encoded_payload is not None:
                try:
                    decoded_payload = Signature.s.load_payload(encoded_payload)
                except BadData:
                    pass
        return decoded_payload

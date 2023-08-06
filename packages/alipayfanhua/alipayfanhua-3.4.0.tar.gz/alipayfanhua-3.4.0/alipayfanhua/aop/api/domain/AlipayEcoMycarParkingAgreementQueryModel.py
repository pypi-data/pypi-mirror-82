#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipayfanhua.aop.api.constant.ParamConstants import *


class AlipayEcoMycarParkingAgreementQueryModel(object):

    def __init__(self):
        self._alipay_user_id = None
        self._car_number = None
        self._ver = None

    @property
    def alipay_user_id(self):
        return self._alipay_user_id

    @alipay_user_id.setter
    def alipay_user_id(self, value):
        self._alipay_user_id = value
    @property
    def car_number(self):
        return self._car_number

    @car_number.setter
    def car_number(self, value):
        self._car_number = value
    @property
    def ver(self):
        return self._ver

    @ver.setter
    def ver(self, value):
        self._ver = value


    def to_alipay_dict(self):
        params = dict()
        if self.alipay_user_id:
            if hasattr(self.alipay_user_id, 'to_alipay_dict'):
                params['alipay_user_id'] = self.alipay_user_id.to_alipay_dict()
            else:
                params['alipay_user_id'] = self.alipay_user_id
        if self.car_number:
            if hasattr(self.car_number, 'to_alipay_dict'):
                params['car_number'] = self.car_number.to_alipay_dict()
            else:
                params['car_number'] = self.car_number
        if self.ver:
            if hasattr(self.ver, 'to_alipay_dict'):
                params['ver'] = self.ver.to_alipay_dict()
            else:
                params['ver'] = self.ver
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = AlipayEcoMycarParkingAgreementQueryModel()
        if 'alipay_user_id' in d:
            o.alipay_user_id = d['alipay_user_id']
        if 'car_number' in d:
            o.car_number = d['car_number']
        if 'ver' in d:
            o.ver = d['ver']
        return o



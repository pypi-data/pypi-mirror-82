#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipayfanhua.aop.api.constant.ParamConstants import *


class MybankPaymentTradeNormalpayOrderCreateModel(object):

    def __init__(self):
        self._amount = None
        self._biz_channel = None
        self._biz_no = None
        self._card_no = None
        self._currency_value = None
        self._ext_info = None
        self._ipid = None
        self._iproleid = None
        self._order_type = None
        self._payee_fund_detail = None
        self._payer_fund_detail = None
        self._request_no = None
        self._request_time = None

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value
    @property
    def biz_channel(self):
        return self._biz_channel

    @biz_channel.setter
    def biz_channel(self, value):
        self._biz_channel = value
    @property
    def biz_no(self):
        return self._biz_no

    @biz_no.setter
    def biz_no(self, value):
        self._biz_no = value
    @property
    def card_no(self):
        return self._card_no

    @card_no.setter
    def card_no(self, value):
        self._card_no = value
    @property
    def currency_value(self):
        return self._currency_value

    @currency_value.setter
    def currency_value(self, value):
        self._currency_value = value
    @property
    def ext_info(self):
        return self._ext_info

    @ext_info.setter
    def ext_info(self, value):
        self._ext_info = value
    @property
    def ipid(self):
        return self._ipid

    @ipid.setter
    def ipid(self, value):
        self._ipid = value
    @property
    def iproleid(self):
        return self._iproleid

    @iproleid.setter
    def iproleid(self, value):
        self._iproleid = value
    @property
    def order_type(self):
        return self._order_type

    @order_type.setter
    def order_type(self, value):
        self._order_type = value
    @property
    def payee_fund_detail(self):
        return self._payee_fund_detail

    @payee_fund_detail.setter
    def payee_fund_detail(self, value):
        self._payee_fund_detail = value
    @property
    def payer_fund_detail(self):
        return self._payer_fund_detail

    @payer_fund_detail.setter
    def payer_fund_detail(self, value):
        self._payer_fund_detail = value
    @property
    def request_no(self):
        return self._request_no

    @request_no.setter
    def request_no(self, value):
        self._request_no = value
    @property
    def request_time(self):
        return self._request_time

    @request_time.setter
    def request_time(self, value):
        self._request_time = value


    def to_alipay_dict(self):
        params = dict()
        if self.amount:
            if hasattr(self.amount, 'to_alipay_dict'):
                params['amount'] = self.amount.to_alipay_dict()
            else:
                params['amount'] = self.amount
        if self.biz_channel:
            if hasattr(self.biz_channel, 'to_alipay_dict'):
                params['biz_channel'] = self.biz_channel.to_alipay_dict()
            else:
                params['biz_channel'] = self.biz_channel
        if self.biz_no:
            if hasattr(self.biz_no, 'to_alipay_dict'):
                params['biz_no'] = self.biz_no.to_alipay_dict()
            else:
                params['biz_no'] = self.biz_no
        if self.card_no:
            if hasattr(self.card_no, 'to_alipay_dict'):
                params['card_no'] = self.card_no.to_alipay_dict()
            else:
                params['card_no'] = self.card_no
        if self.currency_value:
            if hasattr(self.currency_value, 'to_alipay_dict'):
                params['currency_value'] = self.currency_value.to_alipay_dict()
            else:
                params['currency_value'] = self.currency_value
        if self.ext_info:
            if hasattr(self.ext_info, 'to_alipay_dict'):
                params['ext_info'] = self.ext_info.to_alipay_dict()
            else:
                params['ext_info'] = self.ext_info
        if self.ipid:
            if hasattr(self.ipid, 'to_alipay_dict'):
                params['ipid'] = self.ipid.to_alipay_dict()
            else:
                params['ipid'] = self.ipid
        if self.iproleid:
            if hasattr(self.iproleid, 'to_alipay_dict'):
                params['iproleid'] = self.iproleid.to_alipay_dict()
            else:
                params['iproleid'] = self.iproleid
        if self.order_type:
            if hasattr(self.order_type, 'to_alipay_dict'):
                params['order_type'] = self.order_type.to_alipay_dict()
            else:
                params['order_type'] = self.order_type
        if self.payee_fund_detail:
            if hasattr(self.payee_fund_detail, 'to_alipay_dict'):
                params['payee_fund_detail'] = self.payee_fund_detail.to_alipay_dict()
            else:
                params['payee_fund_detail'] = self.payee_fund_detail
        if self.payer_fund_detail:
            if hasattr(self.payer_fund_detail, 'to_alipay_dict'):
                params['payer_fund_detail'] = self.payer_fund_detail.to_alipay_dict()
            else:
                params['payer_fund_detail'] = self.payer_fund_detail
        if self.request_no:
            if hasattr(self.request_no, 'to_alipay_dict'):
                params['request_no'] = self.request_no.to_alipay_dict()
            else:
                params['request_no'] = self.request_no
        if self.request_time:
            if hasattr(self.request_time, 'to_alipay_dict'):
                params['request_time'] = self.request_time.to_alipay_dict()
            else:
                params['request_time'] = self.request_time
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = MybankPaymentTradeNormalpayOrderCreateModel()
        if 'amount' in d:
            o.amount = d['amount']
        if 'biz_channel' in d:
            o.biz_channel = d['biz_channel']
        if 'biz_no' in d:
            o.biz_no = d['biz_no']
        if 'card_no' in d:
            o.card_no = d['card_no']
        if 'currency_value' in d:
            o.currency_value = d['currency_value']
        if 'ext_info' in d:
            o.ext_info = d['ext_info']
        if 'ipid' in d:
            o.ipid = d['ipid']
        if 'iproleid' in d:
            o.iproleid = d['iproleid']
        if 'order_type' in d:
            o.order_type = d['order_type']
        if 'payee_fund_detail' in d:
            o.payee_fund_detail = d['payee_fund_detail']
        if 'payer_fund_detail' in d:
            o.payer_fund_detail = d['payer_fund_detail']
        if 'request_no' in d:
            o.request_no = d['request_no']
        if 'request_time' in d:
            o.request_time = d['request_time']
        return o



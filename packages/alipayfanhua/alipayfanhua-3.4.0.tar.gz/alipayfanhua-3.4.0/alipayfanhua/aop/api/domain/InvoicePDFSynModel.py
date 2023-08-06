#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipayfanhua.aop.api.constant.ParamConstants import *


class InvoicePDFSynModel(object):

    def __init__(self):
        self._extend_fields = None
        self._file_download_type = None
        self._file_download_url = None
        self._out_invoice_id = None
        self._user_id = None

    @property
    def extend_fields(self):
        return self._extend_fields

    @extend_fields.setter
    def extend_fields(self, value):
        self._extend_fields = value
    @property
    def file_download_type(self):
        return self._file_download_type

    @file_download_type.setter
    def file_download_type(self, value):
        self._file_download_type = value
    @property
    def file_download_url(self):
        return self._file_download_url

    @file_download_url.setter
    def file_download_url(self, value):
        self._file_download_url = value
    @property
    def out_invoice_id(self):
        return self._out_invoice_id

    @out_invoice_id.setter
    def out_invoice_id(self, value):
        self._out_invoice_id = value
    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value


    def to_alipay_dict(self):
        params = dict()
        if self.extend_fields:
            if hasattr(self.extend_fields, 'to_alipay_dict'):
                params['extend_fields'] = self.extend_fields.to_alipay_dict()
            else:
                params['extend_fields'] = self.extend_fields
        if self.file_download_type:
            if hasattr(self.file_download_type, 'to_alipay_dict'):
                params['file_download_type'] = self.file_download_type.to_alipay_dict()
            else:
                params['file_download_type'] = self.file_download_type
        if self.file_download_url:
            if hasattr(self.file_download_url, 'to_alipay_dict'):
                params['file_download_url'] = self.file_download_url.to_alipay_dict()
            else:
                params['file_download_url'] = self.file_download_url
        if self.out_invoice_id:
            if hasattr(self.out_invoice_id, 'to_alipay_dict'):
                params['out_invoice_id'] = self.out_invoice_id.to_alipay_dict()
            else:
                params['out_invoice_id'] = self.out_invoice_id
        if self.user_id:
            if hasattr(self.user_id, 'to_alipay_dict'):
                params['user_id'] = self.user_id.to_alipay_dict()
            else:
                params['user_id'] = self.user_id
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = InvoicePDFSynModel()
        if 'extend_fields' in d:
            o.extend_fields = d['extend_fields']
        if 'file_download_type' in d:
            o.file_download_type = d['file_download_type']
        if 'file_download_url' in d:
            o.file_download_url = d['file_download_url']
        if 'out_invoice_id' in d:
            o.out_invoice_id = d['out_invoice_id']
        if 'user_id' in d:
            o.user_id = d['user_id']
        return o



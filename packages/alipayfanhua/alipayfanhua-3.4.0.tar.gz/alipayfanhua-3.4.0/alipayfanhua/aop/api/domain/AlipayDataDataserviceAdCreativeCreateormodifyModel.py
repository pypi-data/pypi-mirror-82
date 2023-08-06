#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipayfanhua.aop.api.constant.ParamConstants import *
from alipayfanhua.aop.api.domain.ActionProperty import ActionProperty
from alipayfanhua.aop.api.domain.MaterialUnit import MaterialUnit


class AlipayDataDataserviceAdCreativeCreateormodifyModel(object):

    def __init__(self):
        self._action_property_list = None
        self._action_type = None
        self._batch_tag = None
        self._biz_token = None
        self._creative_outer_id = None
        self._extend_info = None
        self._group_outer_id = None
        self._lbs_list = None
        self._material_list = None
        self._name = None
        self._region_list = None
        self._status = None
        self._store_id = None
        self._target_app_id = None
        self._target_url = None
        self._template_id = None

    @property
    def action_property_list(self):
        return self._action_property_list

    @action_property_list.setter
    def action_property_list(self, value):
        if isinstance(value, list):
            self._action_property_list = list()
            for i in value:
                if isinstance(i, ActionProperty):
                    self._action_property_list.append(i)
                else:
                    self._action_property_list.append(ActionProperty.from_alipay_dict(i))
    @property
    def action_type(self):
        return self._action_type

    @action_type.setter
    def action_type(self, value):
        self._action_type = value
    @property
    def batch_tag(self):
        return self._batch_tag

    @batch_tag.setter
    def batch_tag(self, value):
        self._batch_tag = value
    @property
    def biz_token(self):
        return self._biz_token

    @biz_token.setter
    def biz_token(self, value):
        self._biz_token = value
    @property
    def creative_outer_id(self):
        return self._creative_outer_id

    @creative_outer_id.setter
    def creative_outer_id(self, value):
        self._creative_outer_id = value
    @property
    def extend_info(self):
        return self._extend_info

    @extend_info.setter
    def extend_info(self, value):
        self._extend_info = value
    @property
    def group_outer_id(self):
        return self._group_outer_id

    @group_outer_id.setter
    def group_outer_id(self, value):
        self._group_outer_id = value
    @property
    def lbs_list(self):
        return self._lbs_list

    @lbs_list.setter
    def lbs_list(self, value):
        if isinstance(value, list):
            self._lbs_list = list()
            for i in value:
                self._lbs_list.append(i)
    @property
    def material_list(self):
        return self._material_list

    @material_list.setter
    def material_list(self, value):
        if isinstance(value, list):
            self._material_list = list()
            for i in value:
                if isinstance(i, MaterialUnit):
                    self._material_list.append(i)
                else:
                    self._material_list.append(MaterialUnit.from_alipay_dict(i))
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    @property
    def region_list(self):
        return self._region_list

    @region_list.setter
    def region_list(self, value):
        if isinstance(value, list):
            self._region_list = list()
            for i in value:
                self._region_list.append(i)
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
    @property
    def store_id(self):
        return self._store_id

    @store_id.setter
    def store_id(self, value):
        self._store_id = value
    @property
    def target_app_id(self):
        return self._target_app_id

    @target_app_id.setter
    def target_app_id(self, value):
        self._target_app_id = value
    @property
    def target_url(self):
        return self._target_url

    @target_url.setter
    def target_url(self, value):
        self._target_url = value
    @property
    def template_id(self):
        return self._template_id

    @template_id.setter
    def template_id(self, value):
        self._template_id = value


    def to_alipay_dict(self):
        params = dict()
        if self.action_property_list:
            if isinstance(self.action_property_list, list):
                for i in range(0, len(self.action_property_list)):
                    element = self.action_property_list[i]
                    if hasattr(element, 'to_alipay_dict'):
                        self.action_property_list[i] = element.to_alipay_dict()
            if hasattr(self.action_property_list, 'to_alipay_dict'):
                params['action_property_list'] = self.action_property_list.to_alipay_dict()
            else:
                params['action_property_list'] = self.action_property_list
        if self.action_type:
            if hasattr(self.action_type, 'to_alipay_dict'):
                params['action_type'] = self.action_type.to_alipay_dict()
            else:
                params['action_type'] = self.action_type
        if self.batch_tag:
            if hasattr(self.batch_tag, 'to_alipay_dict'):
                params['batch_tag'] = self.batch_tag.to_alipay_dict()
            else:
                params['batch_tag'] = self.batch_tag
        if self.biz_token:
            if hasattr(self.biz_token, 'to_alipay_dict'):
                params['biz_token'] = self.biz_token.to_alipay_dict()
            else:
                params['biz_token'] = self.biz_token
        if self.creative_outer_id:
            if hasattr(self.creative_outer_id, 'to_alipay_dict'):
                params['creative_outer_id'] = self.creative_outer_id.to_alipay_dict()
            else:
                params['creative_outer_id'] = self.creative_outer_id
        if self.extend_info:
            if hasattr(self.extend_info, 'to_alipay_dict'):
                params['extend_info'] = self.extend_info.to_alipay_dict()
            else:
                params['extend_info'] = self.extend_info
        if self.group_outer_id:
            if hasattr(self.group_outer_id, 'to_alipay_dict'):
                params['group_outer_id'] = self.group_outer_id.to_alipay_dict()
            else:
                params['group_outer_id'] = self.group_outer_id
        if self.lbs_list:
            if isinstance(self.lbs_list, list):
                for i in range(0, len(self.lbs_list)):
                    element = self.lbs_list[i]
                    if hasattr(element, 'to_alipay_dict'):
                        self.lbs_list[i] = element.to_alipay_dict()
            if hasattr(self.lbs_list, 'to_alipay_dict'):
                params['lbs_list'] = self.lbs_list.to_alipay_dict()
            else:
                params['lbs_list'] = self.lbs_list
        if self.material_list:
            if isinstance(self.material_list, list):
                for i in range(0, len(self.material_list)):
                    element = self.material_list[i]
                    if hasattr(element, 'to_alipay_dict'):
                        self.material_list[i] = element.to_alipay_dict()
            if hasattr(self.material_list, 'to_alipay_dict'):
                params['material_list'] = self.material_list.to_alipay_dict()
            else:
                params['material_list'] = self.material_list
        if self.name:
            if hasattr(self.name, 'to_alipay_dict'):
                params['name'] = self.name.to_alipay_dict()
            else:
                params['name'] = self.name
        if self.region_list:
            if isinstance(self.region_list, list):
                for i in range(0, len(self.region_list)):
                    element = self.region_list[i]
                    if hasattr(element, 'to_alipay_dict'):
                        self.region_list[i] = element.to_alipay_dict()
            if hasattr(self.region_list, 'to_alipay_dict'):
                params['region_list'] = self.region_list.to_alipay_dict()
            else:
                params['region_list'] = self.region_list
        if self.status:
            if hasattr(self.status, 'to_alipay_dict'):
                params['status'] = self.status.to_alipay_dict()
            else:
                params['status'] = self.status
        if self.store_id:
            if hasattr(self.store_id, 'to_alipay_dict'):
                params['store_id'] = self.store_id.to_alipay_dict()
            else:
                params['store_id'] = self.store_id
        if self.target_app_id:
            if hasattr(self.target_app_id, 'to_alipay_dict'):
                params['target_app_id'] = self.target_app_id.to_alipay_dict()
            else:
                params['target_app_id'] = self.target_app_id
        if self.target_url:
            if hasattr(self.target_url, 'to_alipay_dict'):
                params['target_url'] = self.target_url.to_alipay_dict()
            else:
                params['target_url'] = self.target_url
        if self.template_id:
            if hasattr(self.template_id, 'to_alipay_dict'):
                params['template_id'] = self.template_id.to_alipay_dict()
            else:
                params['template_id'] = self.template_id
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = AlipayDataDataserviceAdCreativeCreateormodifyModel()
        if 'action_property_list' in d:
            o.action_property_list = d['action_property_list']
        if 'action_type' in d:
            o.action_type = d['action_type']
        if 'batch_tag' in d:
            o.batch_tag = d['batch_tag']
        if 'biz_token' in d:
            o.biz_token = d['biz_token']
        if 'creative_outer_id' in d:
            o.creative_outer_id = d['creative_outer_id']
        if 'extend_info' in d:
            o.extend_info = d['extend_info']
        if 'group_outer_id' in d:
            o.group_outer_id = d['group_outer_id']
        if 'lbs_list' in d:
            o.lbs_list = d['lbs_list']
        if 'material_list' in d:
            o.material_list = d['material_list']
        if 'name' in d:
            o.name = d['name']
        if 'region_list' in d:
            o.region_list = d['region_list']
        if 'status' in d:
            o.status = d['status']
        if 'store_id' in d:
            o.store_id = d['store_id']
        if 'target_app_id' in d:
            o.target_app_id = d['target_app_id']
        if 'target_url' in d:
            o.target_url = d['target_url']
        if 'template_id' in d:
            o.template_id = d['template_id']
        return o



#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipayfanhua.aop.api.response.AlipayResponse import AlipayResponse


class AlipayOpenMiniInnerversionUploadstatusQueryResponse(AlipayResponse):

    def __init__(self):
        super(AlipayOpenMiniInnerversionUploadstatusQueryResponse, self).__init__()
        self._build_info = None
        self._build_package_url = None
        self._build_status = None
        self._need_rotation = None
        self._version_created = None

    @property
    def build_info(self):
        return self._build_info

    @build_info.setter
    def build_info(self, value):
        self._build_info = value
    @property
    def build_package_url(self):
        return self._build_package_url

    @build_package_url.setter
    def build_package_url(self, value):
        self._build_package_url = value
    @property
    def build_status(self):
        return self._build_status

    @build_status.setter
    def build_status(self, value):
        self._build_status = value
    @property
    def need_rotation(self):
        return self._need_rotation

    @need_rotation.setter
    def need_rotation(self, value):
        self._need_rotation = value
    @property
    def version_created(self):
        return self._version_created

    @version_created.setter
    def version_created(self, value):
        self._version_created = value

    def parse_response_content(self, response_content):
        response = super(AlipayOpenMiniInnerversionUploadstatusQueryResponse, self).parse_response_content(response_content)
        if 'build_info' in response:
            self.build_info = response['build_info']
        if 'build_package_url' in response:
            self.build_package_url = response['build_package_url']
        if 'build_status' in response:
            self.build_status = response['build_status']
        if 'need_rotation' in response:
            self.need_rotation = response['need_rotation']
        if 'version_created' in response:
            self.version_created = response['version_created']

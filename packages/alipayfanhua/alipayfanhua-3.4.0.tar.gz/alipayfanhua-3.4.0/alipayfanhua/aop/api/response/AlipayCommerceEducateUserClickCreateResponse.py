#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipayfanhua.aop.api.response.AlipayResponse import AlipayResponse


class AlipayCommerceEducateUserClickCreateResponse(AlipayResponse):

    def __init__(self):
        super(AlipayCommerceEducateUserClickCreateResponse, self).__init__()


    def parse_response_content(self, response_content):
        response = super(AlipayCommerceEducateUserClickCreateResponse, self).parse_response_content(response_content)

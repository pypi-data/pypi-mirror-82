#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipayfanhua.aop.api.response.AlipayResponse import AlipayResponse


class AlipayEcoRenthouseRoomConcentrationSyncResponse(AlipayResponse):

    def __init__(self):
        super(AlipayEcoRenthouseRoomConcentrationSyncResponse, self).__init__()


    def parse_response_content(self, response_content):
        response = super(AlipayEcoRenthouseRoomConcentrationSyncResponse, self).parse_response_content(response_content)

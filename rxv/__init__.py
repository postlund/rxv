#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function

import requests
import xml.etree.ElementTree as ET

from .rxv import RXV
from . import ssdp

__all__ = ['RXV']


def find(timeout=1.5):
    """Find all Yamah receivers on local network using SSDP search"""
    return [
        RXV(ctrl_url=ri.ctrl_url, model_name=ri.model_name, friendly_name=ri.friendly_name)
        for ri in ssdp.discover(timeout=timeout)
    ]


def find_all_zones(ip=None, max_zones=0):
    """Create an RXV for every zone found for independent control."""
    r = requests.get("http://%s/YamahaRemoteControl/desc.xml" % ip)
    xml = ET.fromstring(r.content)
    model = xml.find('.').get('Unit_Name')
    zones = xml.findall('.//*[@Func="Subunit"]')
    ctrl_url = "http://%s/YamahaRemoteControl/ctrl" % ip
    return [RXV(ctrl_url, model_name=model, zone=z.get('YNC_Tag'))
                for z in zones]

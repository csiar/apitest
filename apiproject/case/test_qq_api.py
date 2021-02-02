# coding:utf-8

import unittest
import requests
import re

# 前置和后置

class TestQQ(unittest.TestCase):

    def test_qq_01(self):
        url = "http://japi.juhe.cn/qqevaluate/qq"
        par = {
            "key": "",
            "qq": "154646545"
        }
        r = requests.get(url, params=par)
        res = r.json()
        self.assertTrue(res['reason'] == 'KEY ERROR!')


    def test_qq_02(self):
        url = "http://japi.juhe.cn/qqevaluate/qq"
        par = {
            "key": "dsfdasfasfdasfas",
            "qq": "154646545"
        }
        r = requests.get(url, params=par)
        res = r.json()
        self.assertTrue(res['reason'] == 'success')
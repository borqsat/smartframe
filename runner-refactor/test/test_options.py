#!/usr/bin/env python
#coding: utf-8

from stability.impl.options import Options
import unittest

class TestOptions_v0(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testArgs(self):
        args = ['runtest.py', '--plan', 'test.plan', '--cycle', '10', '--product', 'test_sample', '--platform', 'android']
        opt = Options(args)
        self.assertEquals(opt['plan'], 'test.plan')
        self.assertEquals(opt['cycle'], 10)
        self.assertEquals(opt['product'], 'test_sample')
        self.assertEquals(opt['platform'], 'android')
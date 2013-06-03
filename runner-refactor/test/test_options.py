#!/usr/bin/env python  
#coding: utf-8

from stability.impl.v0.options import Options
import unittest


class TestOptions_v0(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testArgs(self):
		args = '--plan testplan.xml --cycle 10'
		args = args.strip().split(' ')
		opt = Options(args).opt
		self.assertEqual(opt.plan, 'testplan.xml')

#!/usr/bin/env python
import unittest

class SampleTest(unittest.TestCase):

    def setUp(self):
        super(SampleTest,self).setUp()

    def testSMSSend(self):
        self.device.touch('200','300')
        #self.device.press('home')
        #self.expect('home.png')

        
    def tearDown(self):
        super(SampleTest,self).tearDown()

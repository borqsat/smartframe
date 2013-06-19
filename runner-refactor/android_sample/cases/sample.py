#!/usr/bin/env python
import unittest

class SampleTest(unittest.TestCase):

    def setUp(self):
        super(SampleTest,self).setUp()

    def testSMSSend(self):
    	self.device.expect(name='app_message.png')
    	self.device.touch_image(name='app_message.png')
    	self.device.expect(name='msg_launch.png')

        #self.device.touch('200','300')
        #self.device.press('home')

        
    def tearDown(self):
        super(SampleTest,self).tearDown()

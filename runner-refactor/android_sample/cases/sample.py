#!/usr/bin/env python
import unittest

class SampleTest(unittest.TestCase):

    def setUp(self):
        super(SampleTest,self).setUp()

    def testSMSSend(self):
        self.device.expect(name='app_message1.png')\
                   .touch_image(name='app_message1.png')\
                   .expect(name='msg_launch1.png')
    
    def testUIAutomator(self):
        self.device.press('back')\
                   .press('back')\
                   .press('home')\
                   .press('menu')\
                   .press('up')\
                   .press('down')\
                   .press('center')

    def tearDown(self):
        self.device.press(key='back').press(key='back').press(key='home')
        super(SampleTest,self).tearDown()

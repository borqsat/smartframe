#!/usr/bin/env python
import unittest

PACKAGE_NAME = 'com.android.mms'
ACTIVITY_NAME = PACKAGE_NAME + '.ui.ConversationList'
SMS_RECEIVER = '13581739891'
SMS_CONTENT = 'testsms'

class SampleTest(unittest.TestCase):

    def setUp(self):
        super(SampleTest,self).setUp()
        self.runComponent = PACKAGE_NAME + '/' + ACTIVITY_NAME

    def testSMSSend(self):
        print 'int to test '
        self.device.press('home')
        self.expect('home.png')

        
    def tearDown(self):
        super(SampleTest,self).tearDown()

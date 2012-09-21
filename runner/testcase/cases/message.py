#!/usr/bin/env python
import unittest
#from stability import DeviceManager
from stability import TestCaseBase

PACKAGE_NAME = 'com.android.mms'
ACTIVITY_NAME = PACKAGE_NAME + '.ui.ConversationList'

class MessageTest(TestCaseBase):         
    #get device
    def setUp(self):
        super(MessageTest,self).setUp()
        self.runComponent = PACKAGE_NAME + '/' + ACTIVITY_NAME

    def testSMSSend(self):
        self.worker.startActivity(component=self.runComponent,flags=0x04000000)\
        .sleep(3)\
        .pressKey('up')\
        .touch(60,372)\
        .sleep(3).waitForScreen(rect=(134./480, 714./800, 340./480, 788./800))

    def tearDown(self):
        self.worker.pressKey('back,back,back')
        super(MessageTest,self).tearDown()        

#!/usr/bin/env python
import unittest
#from stability import DeviceManager
from stability import TestCaseBase

PACKAGE_NAME = 'com.android.contacts'
ACTIVITY_NAME = PACKAGE_NAME + '.DialtactsActivity'
ACTION = 'android.intent.action.DIAL'
PHONE_POINT_DAIL_TAB = (94,73)
PHONE_POINT_END_CALL = (312,862)
PHONE_RECT_CHECK_CALL = (493./600, 84./1024, 528./600, 116./1024)
WAIT_FOR_SCREEN_TIMEOUT=10
WAIT_SHORT_TIME=1

class PhoneTest(TestCaseBase):         

    def setUp(self):
        super(PhoneTest,self).setUp()
        self.runComponent = PACKAGE_NAME + '/' + ACTIVITY_NAME

    def testMOCall(self):
        self.launch(component=self.runComponent,flags=0x04000000)\
        .check()\
        .check()\
        .check()\

    def testMOCall000(self):
        self.launch(component=self.runComponent,flags=0x04000000)
        self.waitForScreen(timeout=WAIT_FOR_SCREEN_TIMEOUT,rect=PHONE_RECT_CHECK_CALL)\
        .waitForScreen(timeout=WAIT_FOR_SCREEN_TIMEOUT,rect=PHONE_RECT_CHECK_CALL)\
        .waitForScreen(timeout=WAIT_FOR_SCREEN_TIMEOUT,rect=PHONE_RECT_CHECK_CALL)


    def tearDown(self):
        self.press('back,back,back')
        super(PhoneTest,self).tearDown()        

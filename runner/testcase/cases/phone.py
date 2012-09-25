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
    #get device
    def setUp(self):
        super(PhoneTest,self).setUp()
        self.runComponent = PACKAGE_NAME + '/' + ACTIVITY_NAME

    def testMOCall(self):
        self.worker.startActivity(component=self.runComponent,flags=0x04000000)\
        .sleep(3)\
        .touch(PHONE_POINT_DAIL_TAB[0],PHONE_POINT_DAIL_TAB[1])\
        .typeWord('10086')\
        .sleep(2)\
        .touch(292,960)\
        .sleep(5)\
        .waitForScreen(timeout=WAIT_FOR_SCREEN_TIMEOUT,rect=PHONE_RECT_CHECK_CALL)
        self.worker.touch(PHONE_POINT_END_CALL[0], PHONE_POINT_END_CALL[1])

    def tearDown(self):
        self.worker.pressKey('back,back,back')
        super(PhoneTest,self).tearDown()        

#!/usr/bin/env python
import unittest

PACKAGE_NAME = 'com.android.contacts'
ACTIVITY_NAME = PACKAGE_NAME + '.DialtactsActivity'
ACTION = 'android.intent.action.DIAL'
PHONE_POINT_DAIL_TAB = (94,73)
PHONE_POINT_END_CALL = (312,862)
PHONE_RECT_CHECK_CALL = (493./600, 84./1024, 528./600, 116./1024)
WAIT_FOR_SCREEN_TIMEOUT=10
WAIT_SHORT_TIME=1

class PhoneTest(unittest.TestCase):

    def setUp(self):
        super(PhoneTest,self).setUp()
        self.runComponent = PACKAGE_NAME + '/' + ACTIVITY_NAME

    #auto check point
    def TOtestMOCall123(self):
        self.launch(component=self.runComponent,flags=0x04000000)\
        .sleep(3)\
        .expect()\
        .input('123456')\
        .sleep(3)\
        .expect()\
        .touch(300,956)\
        .sleep(3)\
        .expect()

    def testMOCall(self):
        self.launch(component=self.runComponent,flags=0x04000000)\
        .sleep(3)\
        .expect('IMG_ACTIVITY_CHECK')\
        .input('123456')\
        .sleep(3)\
        .expect('IMG_INPUT_CHECK')\
        .touch(300,956)\
        .sleep(3)\
        .expect('IMG_CALL_CHECK')


    def testMOCall0000(self):
        self.launch(component=self.runComponent,flags=0x04000000)\
        .expect('CHECK_RECT_1')\
        .touch('BTN_CALL')\
        .expect('CHECK_RECT_2')\
        .press('menu')\
        .expect('CHECK_RECT_3')

    def testMOCall0000000(self):
        self.launch(component=self.runComponent,flags=0x04000000)
        self.waitForScreen(timeout=WAIT_FOR_SCREEN_TIMEOUT,rect=PHONE_RECT_CHECK_CALL)\
        .waitForScreen(timeout=WAIT_FOR_SCREEN_TIMEOUT,rect=PHONE_RECT_CHECK_CALL)\
        .waitForScreen(timeout=WAIT_FOR_SCREEN_TIMEOUT,rect=PHONE_RECT_CHECK_CALL)


    def tearDown(self):
        self.press('back,back,back')
        super(PhoneTest,self).tearDown()

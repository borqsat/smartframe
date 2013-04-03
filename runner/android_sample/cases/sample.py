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
        self.launch(component=self.runComponent)
        if not self.exists('msg_launch.png',interval=2,timeout=4,similarity=0.5):
            self.press('menu')\
            .touch('msg_menu_delete.png')\
            .touch('msg_dialog_delete.png')
        self.expect('msg_launch.png',similarity=1.0,msg='msg launch failed!')\
        .touch('msg_create.png',similarity=0.9,waittime=1)\
        .input(SMS_RECEIVER,2)\
        .touch('msg_content_rect.png',waittime=2)\
        .input(SMS_CONTENT,waittime=3)\
        .touch('msg_send.png')\
        .expect('msg_send_ok.png',interval=5,timeout=10,msg='SMS send failed!')
        
    def tearDown(self):
        self.press('back,back,back')
        super(SampleTest,self).tearDown()

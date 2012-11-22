#!/usr/bin/env python
import unittest

PACKAGE_NAME = 'com.android.mms'
ACTIVITY_NAME = PACKAGE_NAME + '.ui.ConversationList'
SMS_RECEIVER = '13581739891'
SMS_CONTENT = 'testsms'

class MessageTest(unittest.TestCase):

    def setUp(self):
        super(MessageTest,self).setUp()
        self.runComponent = PACKAGE_NAME + '/' + ACTIVITY_NAME

    def testSMSSend(self):
        self.launch(component=self.runComponent,waittime=1)
        if not self.exists('msg_launch.png',interval=2,timeout=4):
            self.press('menu')\
            .touch('msg_menu_delete.png')\
            .touch('msg_dialog_delete.png')
        self.expect('msg_launch.png')\
        .touch('msg_create.png',1)\
        .input(SMS_RECEIVER,2)\
        .touch('msg_content_rect.png',waittime=2)\
        .input(SMS_CONTENT,waittime=3)\
        .touch('msg_send.png')\
        .expect('msg_send_ok.png',interval=5,timeout=10)
        
    def tearDown(self):
        self.press('back,back,back')
        super(MessageTest,self).tearDown()

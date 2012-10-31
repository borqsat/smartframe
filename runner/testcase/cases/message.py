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
        self.launch(component=self.runComponent)
        if not self.exists('msg_launch.png'):
            self.press('menu')\
            .touch('msg_menu_delete.png')\
            .touch('msg_dialog_delete.png')
        self.expect('msg_launch.png')\
        .touch('msg_create.png')\
        .input(SMS_RECEIVER)\
        .touch('msg_content_rect.png')\
        .input(SMS_CONTENT)\
        .touch('msg_send.png')\
        .expect('msg_send_ok.png',timeout=15)
        
    def tearDown(self):
        self.press('back,back,back')
        super(MessageTest,self).tearDown()

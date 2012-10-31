#!/usr/bin/env python
import unittest

PACKAGE_NAME = 'com.android.email'
ACTIVITY_NAME ='.activity.Welcome'
#touch(x,y) 
#press('key1,key2')
#input('xyz')
#drag('x,y,z,v')
#expect('expectPictureName')
#exists() return True or False
class EmailTest(unittest.TestCase):
    #get device
    def setUp(self):
        super(EmailTest,self).setUp()
        self.runComponent = PACKAGE_NAME + '/' + ACTIVITY_NAME

    def testSendEmail(self):
        self.launch(self.runComponent)\
        .expect('IMG_LAUNCH_EMAIL')\
        .touch(384,988)\
        .expect('IMG_LAUNCH_SENTBOX')\
        .touch(186,368)
        
    def tearDown(self):
        self.press('back,back,back')
        super(EmailTest,self).tearDown()
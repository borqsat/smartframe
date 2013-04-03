import unittest
'''
:Author:      test
:Since:       OCT 2012
:Version:     0.1
'''

PACKAGE_NAME = ''
ACTIVITY_NAME = PACKAGE_NAME + ''
class TestClassName(unittest.TestCase):
    def setUp(self):
        super(TestClassName,self).setUp()
        self.runComponent = PACKAGE_NAME + '/' + ACTIVITY_NAME

    #edit test case script here
    def testMethodname(self):
        self.launch(self.runComponent)

    def tearDown(self):
        self.press('back,back,back')
        super(TestClassName,self).tearDown()

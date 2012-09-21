#!/usr/bin/env python
import unittest,time
from stability import TestCaseBase

PACKAGE_NAME = 'com.android.mms'
ACTIVITY_NAME = PACKAGE_NAME + '.ui.ConversationList'

class SnapshotTest(TestCaseBase):         
    #get device
    def setUp(self):
        super(SnapshotTest,self).setUp()

    def testSnapshot(self):
        for i in range(500):
            self.worker.saveImage()
            time.sleep(1)
            self.logger.debug('>>snapshot<<')

    def tearDown(self):
        self.worker.pressKey('back,back,back')
        super(SnapshotTest,self).tearDown()
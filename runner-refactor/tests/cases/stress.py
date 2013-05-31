#!/usr/bin/env python

import sys
if sys.path.find('monkeyrunner') != -1:
    from com.android.monkeyrunner import MonkeyRunner as runner
    from com.android.monkeyrunner import MonkeyDevice as device
if sys.path.find('tizenrunner') != -1:
    from com.android.tizenrunner import TizenRunner as runner
    from com.android.tizenrunner import TizenDevice as device

import unittest
import tempfile, os, subprocess, shutil, threading

# Before running stress tests, make sure monkeyrunner/adb are in your PATH env,
# and adb can list your device (cmd: adb devices).
class AndroidStressTests(unittest.TestCase):

    # To run the test:
    # 1. Enter stability home dir.
    # 2. export environment variables required by test, e.g.
    #        export STRESS_SNAPSHOT_LOOP=1000
    # 3. run test:
    #        monkeyrunner runtests.py -t --testcase=tests.stress.StressTests.testStressScreenSnapshot
    #
    def testStressScreenSnapshot(self):
        '''Take snapshot...'''
        loop_name = 'STRESS_SNAPSHOT_LOOP'
        if os.environ.has_key(loop_name):
            loop_str = os.environ[loop_name]
        else:
            loop_str = MonkeyRunner.input(message='Please input the loop number.', initialValue='100000')
        loop = int(loop_str)
        image_name = 'snapshot'#os.path.join(tempfile.gettempdir(), 'snapshot.png')
        print image_name
        for i in range(loop):
            self.logger.debug('Press HOME key to keep LCD ON.')
            self.press('home')
            self.logger.debug('Take snapshot %d/%d' %(i+1,loop))
            self.saveSnapshot(image_name)
            #self.assertTrue(success,'exception during taking snapshot')
            #self.assertTrue(os.path.exists(image_name),'Exception due to file does\' not exists!')



class TizenStressTests(unittest.TestCase):

    # To run the test:
    # 1. Enter stability home dir.
    # 2. export environment variables required by test, e.g.
    #        export STRESS_SNAPSHOT_LOOP=1000
    # 3. run test:
    #        runner runtests.py -t --testcase=tests.stress.StressTests.testStressScreenSnapshot
    #
    def testStressScreenSnapshot(self):
        '''Take snapshot...'''
        loop_name = 'STRESS_SNAPSHOT_LOOP'
        if os.environ.has_key(loop_name):
            loop_str = os.environ[loop_name]
        else:
            loop_str = 100000
        loop = int(loop_str)
        image_name = 'snapshot'#os.path.join(tempfile.gettempdir(), 'snapshot.png')
        print image_name
        for i in range(loop):
            self.logger.debug('Take snapshot %d/%d' %(i+1,loop))
            self.saveSnapshot(image_name)
            #self.assertTrue(success,'exception during taking snapshot')
            #self.assertTrue(os.path.exists(image_name),'Exception due to file does\' not exists!')

    def TODOtestStressSdb(self):
        '''Take snapshot...'''
        loop_name = 'SDB_PULL_LOOP'
        if os.environ.has_key(loop_name):
            loop_str = os.environ[loop_name]
        else:
            loop_str = 100000
        loop = int(loop_str)
        print image_name
        for i in range(loop):
            self.logger.debug('Take snapshot %d/%d' %(i+1,loop))
            ####sdb push test.png /
            ####sdb pull /test.png 



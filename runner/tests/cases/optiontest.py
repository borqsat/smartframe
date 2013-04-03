#!/usr/bin/env python
import unittest,os
from runtest import CommandOptions
INPUT_CONTENT_FULL = ['runtest.py', '--plan', 'tests/plan/plan', '--product', 'tests', '--cycle', '10', '--uploadresult']
INPUT_CONTENT_DEFAULT = ['runtest.py','--product', 'tests']
class CommandOptionsTest(unittest.TestCase):
    '''
    Unit test for runtest module.
    monkeyrunner ut.py
    runner.ut.py
    '''

    def setUp(self):
        self.option1 = CommandOptions(INPUT_CONTENT_FULL).getProperties()
        self.option2 = CommandOptions(INPUT_CONTENT_DEFAULT).getProperties()
    
    def testParseFullOption(self):
        self.assertTrue('tests/plan/plan' == self.option1['plan'])
        self.assertTrue('tests' == self.option1['product'])
        self.assertTrue('10' == self.option1['cycle'])
        self.assertTrue(self.option1['uploadresult'])
        self.assertTrue(self.option1['testing'])
        self.assertFalse(self.option1['recording'])
        self.assertFalse(self.option1['random'])
        self.assertFalse(self.option1['testcase'])
        self.assertFalse(self.option1['user'])
        self.assertFalse(self.option1['password'])
        self.assertFalse(self.option1['screenmonitor'])
        self.assertFalse(self.option1['downloadsnapshot'])

    def testParseDefaultOption(self):
        self.assertFalse(self.option2['plan'])
        self.assertTrue('tests' == self.option2['product'])
        self.assertTrue('1' == self.option2['cycle'])
        self.assertFalse(self.option2['uploadresult'])
        self.assertTrue(self.option2['testing'])
        self.assertFalse(self.option2['recording'])
        self.assertFalse(self.option2['random'])
        self.assertFalse(self.option2['testcase'])
        self.assertFalse(self.option2['user'])
        self.assertFalse(self.option2['password'])
        self.assertFalse(self.option2['screenmonitor'])
        self.assertFalse(self.option2['downloadsnapshot'])
        
        

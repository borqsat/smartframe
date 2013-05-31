#!/usr/bin/env python
import unittest,os
from runtest import CommandOptions
from stability import TestBuilder
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
INPUT_CONTENT_FULL = ['runtest.py', '--plan', 'tests/plan/plan', '--product', 'tests', '--cycle', '10', '--uploadresult']
INPUT_CONTENT_DEFAULT = ['runtest.py','--product', 'tests']
class BuilderTest(unittest.TestCase):
    '''
    Unit test for builder.
    monkeyrunner ut.py
    runner.ut.py
    '''

    def setUp(self):
        self.option1 = CommandOptions(INPUT_CONTENT_FULL).getProperties()
        self.builder1 = TestBuilder.getBuilder(self.option1)

    def testGetBuilder(self):
        builder = TestBuilder.getBuilder()
        self.assertTrue(builder)
        self.assertTrue(builder is self.builder1)

    def testGetWorkspace(self):
        builder1 = TestBuilder.getBuilder()
        builder2 = TestBuilder.getBuilder(self.option1)
        self.assertTrue(builder1)
        self.assertTrue(builder2)
        self.assertTrue(builder1 is builder2)

    def testGetWorkspace(self):
        builder1 = TestBuilder.getBuilder()
        self.assertTrue(WORKSPACE == builder1.getWorkspace())

    def testGetProperties(self):
        builder1 = TestBuilder.getBuilder()
        self.assertTrue('tests' == builder1.getProperty('product'))
        self.assertTrue(builder1.getProperty('uploadresult'))
        self.assertTrue('10' == builder1.getProperty('cycle'))




        
        

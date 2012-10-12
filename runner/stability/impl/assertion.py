#!/usr/bin/env python
import time, sys, os, shutil, datetime, string
from stability.util.log import Logger
from imglib import imglib
class assertion:
    '''Assertion class provides the assert statement in test case'''

    def __init__(self):
        self.failureException = AssertionError
        self.logger = Logger.getLogger()

    def assertTrue(self,expr,msg=None):
        '''Fail the test unless the expression is true.''' 
        if not expr: raise self.failureException, msg

    def assertEqual(self, first, second, msg=None):
        '''Fail if the two objects are unequal as determined by the == operator.'''
        if not first == second:
            raise self.failureException,(msg or '%r != %r' % (first, second))

    def assertExists(self,fullImgPath,subImgPath,msg=None):
        '''Fail if the subImg not contained in fullImg'''    
        imglib.assertExists(fullImgPath,subImgPath)

#!/usr/bin/env python  
#coding: utf-8

'''
Module provides TestRunner and _TestResult class.
TestRunner class for controling the whole test cycle.
_TestResult class extends from unittest.TestResult which holds test result information.
@version: 1.0
@author: borqsat
@see: null
'''

from testresult import TestResultImpl
from ability import Ability
from devicemanager import DeviceManager,BaseDevice
import unittest  
import functools
import inspect

def mixIn(base):
    '''
    Decorator of function. It mixed Ability to BaseDevice
    '''
    def deco(function):
        def wrap(*args, **argkw):        
            setattr(BaseDevice,'result',getattr(args[0],'_result'))
            for name,method in inspect.getmembers(base,predicate=inspect.ismethod):
                if name == 'setUp':
                    setattr(base,name,_inject_setup(base,method))
                if name == 'tearDown':
                    setattr(base,name,_inject_teardown(base,method))                    
            function(*args, **argkw)
        return wrap
    return deco

def _inject_setup(cls,method):
    @functools.wraps(method)
    def wrapped(self,*args,**kwargs):
        try:
            setattr(cls, 'device', DeviceManager.getInstance('android').getDevice())
            method(self, *args, **kwargs)
        except:
            raise
        finally:
            pass
    return wrapped or method

def _inject_teardown(cls,method):
    @functools.wraps(method)
    def wrapped(self,*args,**kwargs):
        try:
            getattr(getattr(cls, 'device'),'destory')()
            method(self, *args, **kwargs)
        except:
            raise
        finally:
            pass
    return wrapped or method

class TestRunner(object):
    '''
    A test runner that control the whole test cycle.
    '''
    def __init__(self,result=None):
        '''
        Init the instance of TestRunner
        @type result: unittest.TestResult.
        @param result: an instance of unittest.TestResult. Holder for test result information
        '''
        self._result = result

    @mixIn(unittest.TestCase)
    def run(self,suites):
        '''
        Wrap the unittest.TestCase class. inject ability to interact with device.
        Run the test suite against the supplied test suites.
        @type list
        @param a list of test case methods
        '''
        #print suites
        for cycle in range(int(self._result.options['cycle'])):
            for test in suites:
                if isinstance(test,unittest.TestSuite):
                    for t in test:
                        t(self._result)
                elif isinstance(test,unittest.TestCase):
                    test(self._result)
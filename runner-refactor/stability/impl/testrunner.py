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
from devicemanager import DeviceManager
import unittest  
import functools
import inspect

def mixIn(base,addition):
    '''
    Decorator of function. It mixed Ability to unittest.TestCase
    '''
    def deco(function):
        def wrap(*args, **argkw):
            assert not hasattr(base, '_mixed_')
            mixed = []
            for item, var in Ability.__dict__.items():
                if not hasattr(base,item):
                    setattr(base,item,var)
                    mixed.append(item)
            base._mixed_ = mixed
            setattr(base,'result',getattr(args[0],'_result')) 
            for name,method in inspect.getmembers(base,predicate=inspect.ismethod):
                if name == 'setUp':
                    setattr(base,name,_injects(base,method))
            function(*args, **argkw)
        return wrap
    return deco

def _injects(cls,method):
    @functools.wraps(method)
    def wrapped(self,*args,**kwargs):
        try:
            setattr(cls, 'device', DeviceManager.getInstance('android').getDevice())
            method(self,*args,**kwargs)
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

    @mixIn(unittest.TestCase, Ability)
    def run(self,tests):
        '''
        Wrap the unittest.TestCase class. inject ability to interact with device.
        Run the test suite against the supplied test suites.
        @type list
        @param a list of test case methods
        '''
        for cycle in range(int(self._result.options['cycle'])):
            for test in tests:
                print type(test)
                test(self._result)
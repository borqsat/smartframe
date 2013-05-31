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
 
    def run(self,tests):
        '''
        Wrap the unittest.TestCase class. inject ability to interact with device.
        Run the test suite against the supplied test suites.
        @type list
        @param a list of test case methods
        '''
        _mixIn(unittest.TestCase,Ability)
        _inject(unittest.TestCase,'device', DeviceManager.getInstance().getDevice())
        _inject(unittest.TestCase,'result', self._result)

        for cycle in range(int(self._result.options['cycle'])):
            for test in tests: test(self._result)

def _inject(cls,attrbuite_name,impl):
    '''
    Inject attribute to the target class
    '''
    setattr(cls,attrbuite_name,impl)

def _mixIn(base,addition):
    '''
    mixed base class with addition class 
    '''
    assert not hasattr(base, '_mixed_')
    mixed = []
    for item, var in Ability.__dict__.items():
        if not hasattr(base,item):
            setattr(base,item,var)
            mixed.append(item)
    base._mixed_ = mixed  

def __mixIn(py_class,mixin_class):
    '''
    mixed py_class with mixin_class
    '''
    if mixin_class not in py_class.__bases__:
        py_class.__bases__ = (mixin_class,) + py_class.__bases__
#!/usr/bin/env python  
#coding: utf-8

'''
Module for maintaining test suite. 
@version: 1.0
@author: borqsat
@see: null
'''

import os 
from collections import OrderedDict
import ConfigParser
import unittest

class TestBuilder(object):
    '''Class for maintaining session properties.'''
    def __init__(self,option):
        '''Init TestBuilder instance'''
        self._option = option
        

    def getTestSuite(self):
        '''
        Return the test suites specified by options argument.
        @rtype: []
        @return: list of instances of unittest.TestCase    
        '''
        if self._option['testcase']:
            return self._getTestSuiteByName(self._option['testcase'])
        if self._option['plan']:
            print 'read from plan file...'
            return self._getTestSuiteFromFile(self._option['plan'])

      
        
    def _getTestSuiteByName(self,name):
        '''
        Return a test object list from the given class. we called it TestSuites. Python unittest 
        A unittest.TestCase instance only contain the target method to be run.
        @rtype: []
        @return: list of instances of unittest.TestCase specified by '--testcase'
        '''

        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(name)
        return suite

    def _getTestSuiteFromFile(self,plan_file_path):
        '''
        Return a test object list from the given plan file. we called it TestSuites. Python unittest 
        A unittest.TestCase instance only contain the target method to be run.
        @rtype: []
        @return: list of instances of unittest.TestCase specified by plan file
        '''
        section_name = 'tests'
        tests = []
        names = []
        loader = unittest.TestLoader()
        parser = ConfigParser.ConfigParser(dict_type=OrderedDict)
        parser.optionxform = lambda x: x
        parser.read(plan_file_path)
        tests = parser.items(section_name)

        for (k,v) in tests:
            for i in range(int(v)):
                names.append(k)
        print names
        suite = loader.loadTestsFromNames(names) 
        return suite

    def _getTestSuiteFromClass(self,class_name):
        '''
        Return a test object list from the given class. we called it TestSuites. Python unittest 
        A unittest.TestCase instance only contain the target method to be run.
        @rtype: []
        @return: list of instances of unittest.TestCase specified by unitest.TestCase class name.
        '''
        pass
        
    def _getTestSuiteFromPackage(self,package_name):
        '''
        Return a test object list from the given package. we called it TestSuites. Python unittest 
        A unittest.TestCase instance only contain the target method to be run.
        @rtype: []
        @return: list of instances of unittest.TestCase specified by test class package
        '''
        pass





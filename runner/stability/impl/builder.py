'''
Module for maintaining session properties and generating test suite. 
@version: 1.0
@author: borqsat
@see: null
'''

import os,sys,string,threading,unittest
from configparser import Parser
from stability.util.log import Logger

class TestBuilder(object):
    '''Class for maintaining session properties.'''
    __instance = None
    __mutex = threading.Lock()
    __buildOption = None
    def __init__(self,properties=None):
        '''Init TestBuilder instance'''
        self.__buildOption = properties
        self.__testLoader = TestLoader()

    def getProperty(self,name):
        '''
        Get the property value of name.
        @rtype: string
        @return: the value of property
        '''
        assert self.__buildOption
        if self.__buildOption.has_key(name):
            value = self.__buildOption[name]
        else:
            raise 'miss data name'
        return value
        
    def getWorkspace(self):
        '''
        Return the test session's report workspace.
        @rtype: string
        @return: the smart runner workspace directory
        '''
        workspace = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return workspace

    @staticmethod
    def getBuilder(option=None):
        '''
        Return a single instance of TestBuilder object.
        @rtype: TestBuilder
        @return: the single instance of TestBuilder
        '''
        if(TestBuilder.__instance == None): 
            TestBuilder.__mutex.acquire()
            if(TestBuilder.__instance == None):
                TestBuilder.__instance = TestBuilder(option)
            else: 
                pass  
            TestBuilder.__mutex.release() 
        else:
            pass     
        return TestBuilder.__instance

    def getTestSuites(self):
        '''
        Return a test object list. we called it TestSuites.
        A unittest.TestCase instance only contain the target method to be run.
        @rtype: unittest.TestSuite
        @return: A instance of TestSuite. a composite test consisting of a number of TestCases    
        '''
        return self.__testLoader.loadTestSuites(self.__buildOption)


class TestLoader(object):
    '''Generate test suites '''
    #testMethodPrefix = 'test' 
    #sortTestMethodsUsing = cmp 
    #suiteClass = TestSuite
    _defaultTestLoader =  unittest.TestLoader
    _defaultParser = Parser
    def __init__(self,loader=None,parser=None):
        '''Init TestLoader instance'''
        if not loader:
            self.loader = TestLoader._defaultTestLoader()
        if not parser:
            self.parser = TestLoader._defaultParser

    def loadTestSuites(self,option):
        '''
        Get test suite.
        @type option: dictionary
        @param option: the properties value of user input from command line.
        @rtype: TestSuite
        @return: a instance of TestSuite.
        '''
        prefix = '%s.%s.' % (option['product'],'cases')
        tests = []
        if option['testcase'] is not None:
            tests.append((option['testcase'], 1))
            return self.__loadSimplyTestSuites(tests,prefix=prefix)
        if option['plan'] is not None:
            tests = self.__readTestCasePlan(option['plan'])
            return self.__loadSimplyTestSuites(tests,prefix=prefix)
        else:
            option['plan'] = '%s%s%s%s%s' % (option['product'],os.sep,'plan',os.sep,'plan')
            tests = self.__readTestCasePlan(option['plan'])
            return self.__loadSimplyTestSuites(tests,prefix=prefix)

    def __readTestCasePlan(self,plan):
        '''
        Get the test case list from plan file.
        @type plan: string
        @param plan: the path of test case plan file.
        @rtype: list
        @return: a list of test case
        '''
        tests = self.parser.getTestConfig(plan)
        return tests

    def __loadTestingTestSuites(self,tests,isRandom=False):
        '''Remove in future'''
        names = []
        t = None
        if type(tests) is type({}):
            t = tests.items()
        elif type(tests) is type([]):
            t = tests
        for (k,v) in t:
            for i in range(v):
                names.append(k)
        print 'list names'
        print names
        ##['','','']
        ###here we can keep test suites sequence.
        suite = self.loader.loadTestsFromNames(names)
        return suite

    def __loadSimplyTestSuites(self,tests,prefix=None,isRandom=False):
        '''
        Return a suite of all tests cases given a string specifier.
        @type tests: list
        @param tests: a list of test cases
        @type prefix: string
        @param prefix: a prefix of test case path
        @type isRandom: boolean
        @param isRandom: If the test case sequence in random order.
        @rtype: unittest.TestSuite
        @return: A instance of TestSuite. a composite test consisting of a number of TestCases speified by test case list.  
        '''
        names = []
        t = None
        if type(tests) is type({}):
            t = tests.items()
        elif type(tests) is type([]):
            t = tests
        for (k,v) in t:
            k = '%s%s' % (prefix,k)
            for i in range(v):
                names.append(k)
        #print 'list names'
        #print names
        suite = self.loader.loadTestsFromNames(names)
        return suite
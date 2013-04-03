'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import os,sys,string,threading,unittest
from configparser import Parser
from stability.util.log import Logger

class TestBuilder(object):
    '''Class for storing test session properties'''
    __instance = None
    __mutex = threading.Lock()
    __buildOption = None
    def __init__(self,properties=None):
        '''
        Init test loader and command-line input properties.
        '''
        self.__buildOption = properties
        self.__testLoader = TestLoader()

    def getProperty(self,name):
        '''Get the value of argument input from command-line'''
        assert self.__buildOption
        if self.__buildOption.has_key(name):
            value = self.__buildOption[name]
        else:
            raise 'miss data name'
        return value
        
    def getWorkspace(self):
        '''Return the test session's report workspace '''
        workspace = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return workspace

    def getLogger(self):
        '''Return a logger instance'''
        #self.__logger = Logger.getLogger('device.log',"INFO","DEBUG")
        self.__logger = Logger.getLogger()
        return self.__logger

    @staticmethod
    def getBuilder(option=None):
        '''Return a single instance of TestBuilder object '''
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
        ''' Return a test object list via test loader. we called it TestSuites.
        test object format:  TestCase.__init__(methodName)
        A unittest.TestCase instance only contain the target method to be run.
        '''
        return self.__testLoader.loadTestSuites(self.__buildOption)


class TestLoader(object):
    '''Class for loading test cases according to the specified path'''
    #testMethodPrefix = 'test' 
    #sortTestMethodsUsing = cmp 
    #suiteClass = TestSuite
    _defaultTestLoader =  unittest.TestLoader
    _defaultParser = Parser
    def __init__(self,loader=None,parser=None):
        '''Init test loader and test parser'''
        if not loader:
            self.loader = TestLoader._defaultTestLoader()
        if not parser:
            self.parser = TestLoader._defaultParser

    def readTestCasePlan(self,plan):
        '''Get the cases plan defination from plan file '''
        tests = self.parser.getTestConfig(plan)
        return tests

    def loadTestSuites(self,option):
        '''return test suite object'''
        prefix = '%s.%s.' % (option['product'],'cases')
        tests = []
        if option['testcase'] is not None:
            tests.append((option['testcase'], 1))
            return self.__loadSimplyTestSuites(tests,prefix=prefix)
        if option['plan'] is not None:
            tests = self.readTestCasePlan(option['plan'])
            return self.__loadSimplyTestSuites(tests,prefix=prefix)
        else:
            option['plan'] = '%s%s%s%s%s' % (option['product'],os.sep,'plan',os.sep,'plan')
            tests = self.readTestCasePlan(option['plan'])
            return self.__loadSimplyTestSuites(tests,prefix=prefix)

    def __loadTestingTestSuites(self,tests,isRandom=False):
        '''Get and random list of test cases object'''
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
        'Get an ordered list of tests cases object with the given string specifier.'
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
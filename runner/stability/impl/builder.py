'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import os,sys,string,threading,unittest
from configparser import ConfigParser
from stability.util.log import Logger

class TestBuilder(object):
    '''Class for storing test session properties'''
    __instance = None
    __mutex = threading.Lock()
    __buildOption = None
    def __init__(self,properties=None):
        self.__buildOption = properties
        self.__testLoader = TestLoader()

    def getProperty(self,name):
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

    def getDeviceSerial(self):
        '''Return the current device serial number '''
        return None

    def getLogger(self):
        '''Return a looger instance'''
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
        ''' Return a test object list. we called it TestSuites.
        test object format:  TestCase.__init__(methodName)
        A unittest.TestCase instance only contain the target method to be run.
        '''
        return self.__createTestSuites()
   
    def __createTestSuites(self):
        tests = []
        # If --testcase option is specified, we will not load tests from config file.
        if self.__buildOption.has_key('testcase'):
            if self.__buildOption['testcase'] is not None:
                tests.append((self.__buildOption['testcase'], 1))
        if self.__buildOption['plan']:
            if self.__buildOption['plan'] is not None:
                tests = self.__testLoader._defaulConfiger.readTests(self.__buildOption['plan'])
        return self.__testLoader.loadTestSuites(tests,self.getProperty('recording'),self.getProperty('random'))

class TestLoader(object):
    #testMethodPrefix = 'test' 
    #sortTestMethodsUsing = cmp 
    #suiteClass = TestSuite
    _defaultTestLoader =  unittest.TestLoader
    _defaulConfiger = ConfigParser
    def __init__(self,loader=None):
        if not loader:
            self.loader = TestLoader._defaultTestLoader()

    def loadTestSuites(self,tests,mode,isRandom=False):
        suites = None
        if mode:
            suites = self.__loadRecordingTestSuites(tests)
        else:
            suites = self.__loadTestingTestSuites(tests)
        return suites

    def __loadRecordingTestSuites(self,tests,isRandom=False):
        names = []
        t = None
        if type(tests) is type({}):
            t = tests.items()
        elif type(tests) is type([]):
            t = tests
        for (k,v) in t:
            names.append(k)
        suite = self.loader.loadTestsFromNames(names)
        return suite

    def __loadTestingTestSuites(self,tests,isRandom=False):
        names = []
        t = None
        if type(tests) is type({}):
            t = tests.items()
        elif type(tests) is type([]):
            t = tests
        for (k,v) in t:
            for i in range(v):
                names.append(k)
        ###here we can keep test suites sequence.
        suite = self.loader.loadTestsFromNames(names)
        return suite

class TestParser(object):
    pass
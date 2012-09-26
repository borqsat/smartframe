import os,sys,string
import threading
import unittest
from configparser import ConfigParser
from stability.util.log import Logger

class TestBuilder(object):
    '''Class for store test session properties '''
    __instance = None
    __mutex = threading.Lock()
    __buildOption = None
    def __init__(self,options=None):
        self.__buildOption = options
        self.__testLoader = TestLoader()

    def getProperty(self,attr):
        assert self.__buildOption

        return ''
        
    def setBuildOption(self,option):
        '''Set an instance of CommandOption object which represent user commandline input'''
        self.__buildOption = option

    def getStartTime(self):
        '''Return the test session start time'''
        return self.__buildOption.starttime
        
    def getWorkspace(self):
        '''Return the test session's report workspace '''
        workspace = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'report')
        if not os.path.exists(workspace):
            os.makedirs(workspace)
                         
        #report_folder_name = ('%s-%s'%('result',self.__buildOption.starttime))
        #report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'report',report_folder_name)
        #report_path = os.path.join(workspace,report_folder_name)
        #if not os.path.exists(report_path):
        #    os.makedirs(report_path)
        return workspace

    def getDeviceSerial(self):
        '''Return the device serial number '''
        return None

    def getLogger(self):
        '''Return a looger instance'''
        #self.__logger = Logger.getLogger('device.log',"INFO","DEBUG")
        self.__logger = Logger.getLogger()
        return self.__logger

    def getCycle(self):
        '''Return the cycle count of test session'''
        return self.__buildOption.cycle

    def isRecording(self):
        '''Return true if the session is recording and otherwise return false'''
        return self.__buildOption.recording

    def isTesting(self):
        '''Return true is the session is testing and otherwise return false'''
        if self.__buildOption.testing:
            return True

    def isScreenMonitor(self):
        '''Return true if the session support screen monitor feature '''
        return self.__buildOption.screenmonitor

    def isUploadResult(self):
        '''Return true if the session support uploading result to server feature '''
        return self.__buildOption.uploadresult

    def isLocalResult(self):
        '''Return true if the session support to save test result in local'''
        return False

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
        return self.createTestSuites()
   
    def createTestSuites(self):
        return self.__testLoader.loadTestSuites(self.__buildOption.plan,self.__buildOption.recording,self.__buildOption.random)

class TestLoader(object):
    #testMethodPrefix = 'test' 
    #sortTestMethodsUsing = cmp 
    #suiteClass = TestSuite 
    _defaultTestLoader =  unittest.TestLoader
    _defaulConfiger = ConfigParser
    def __init__(self,loader=None):
        if not loader:
            self.loader = TestLoader._defaultTestLoader()

    def loadTestSuites(self,path,mode,isRandom=False):
        tests = None
        suites = None
        if path:
            tests = TestLoader._defaulConfiger.readTests(path)
        assert tests, 'tests should not be null!'
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
        suite = self.loader.loadTestsFromNames(names)
        return suite

class TestParser(object):
    pass

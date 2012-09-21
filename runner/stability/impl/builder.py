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
                         
        report_folder_name = ('%s-%s'%('result',self.__buildOption.starttime))
        report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'report',report_folder_name)
        report_path = os.path.join(workspace,report_folder_name)
        if not os.path.exists(report_path):
            os.makedirs(report_path)
        return workspace

    def getTests(self):
        '''Return the test case list specified by plan file '''
        tests = ConfigParser.readTests(self.__buildOption.plan)
        return tests

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
        if self.__buildOption.recording and self.__buildOption.testing:
            return True
            
        if self.__buildOption.recording:
            return True

        if self.__buildOption.testing:
            return False

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

    def loadTestSuites(self):
        if self.isRecording:
            return self.__loadRecordingTestSuites(self.getTests())
        if self.isTesting:
            return self.__loadTestingTestSuites(self.getTests())

    def __loadRecordingTestSuites(self,tests):
        names = []
        t = None
        if type(tests) is type({}):
            t = tests.items()
        elif type(tests) is type([]):
            t = tests
        for (k,v) in t:
            names.append(k)
        suite = unittest.TestLoader().loadTestsFromNames(names)
        return suite
     
    def __loadTestingTestSuites(self,tests):
        names = []
        t = None
        if type(tests) is type({}):
            t = tests.items()
        elif type(tests) is type([]):
            t = tests
        for (k,v) in t:
            for i in range(v):
                names.append(k)
        suite = unittest.TestLoader().loadTestsFromNames(names)
        return suite
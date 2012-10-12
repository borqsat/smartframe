import sys,time,os
import unittest
from unittest import TestResult
from pubsub import pub
from stability.util.log import Logger
from testworker import testWorker
from builder import TestBuilder
from stability.util.log import Logger
from expectresult import ExpectResult

class TestRunner(object):
    '''
    Class for loading test runner
    '''
    def __init__(self,option=None):
        self.logger = Logger.getLogger()
        self.options = option
        self.worker = testWorker(option)
        self.testResult = _TestResult()

    def runTest(self,test_suites):
        self.logger.debug('run the testsuite!!')
        if self.options['recording']:
            self.logger.debug('test mode: recording')
            for test in test_suites:
                self.worker.run(test,self.testResult)
            self.logger.debug('recording end')

        if self.options['testing']:
            self.logger.debug('test mode: testing')
            for cycle in range(int(self.options['cycle'])):
                self.logger.debug('start cycle: ' + str(cycle))
                for test in test_suites:
                    case_name = '%s.%s' %(type( test).__name__,  test._testMethodName)
                    expResultPath = os.path.join(self.testResult.dirs['ws_right'],case_name)
                    expResult = ExpectResult(expResultPath)
                    self.worker.run(test,self.testResult,expResult)
                self.logger.debug('end cycle: ' + str(cycle))

def collectResult(func):
    def wrap(*args, **argkw):
        func(*args, **argkw)
        if True:
            content = (func.__name__,args)
            pub.sendMessage('collectresult',info=content)
        return func
    return wrap

class _TestResult(TestResult):
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream=None, descriptions=None, verbosity=None):
        TestResult.__init__(self)
        self.logger = Logger.getLogger()
        self.builder = TestBuilder.getBuilder()
        #self.sessionStartTime = time.strftime('%Y.%m.%d-%H.%M.%S',time.localtime(time.time()))
        self._initTestResultDir()

    @collectResult
    def startTest(self, test):
        TestResult.startTest(self, test)
        self._createDir(test)
        self.logger.debug(self.getDescription(test))
        self.logger.debug("START")
    
    @collectResult   
    def addSuccess(self,test):
        TestResult.addSuccess(self, test)
        self.logger.debug("PASS")
            
    @collectResult
    def addFailure(self,test,err):
        TestResult.addFailure(self, test, err)
        self.logger.debug("FAIL")
     
    @collectResult    
    def addError(self, test, err):
        TestResult.addError(self, test, err)
        self.logger.debug("ERROR")

    #@writeResult
    def stopTest(self, test):
        TestResult.stopTest(self, test)
        self.logger.debug('STOP')

    def getDescription(self, test):
        return test.shortDescription() or str(test)
            
    def printErrors(self):
        self.printErrorList('ERROR', self.errors) 
        self.printErrorList('FAIL', self.failures)
  
    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.logger.debug(self.separator1)
            self.logger.debug("%s: %s" % (flavour,self.getDescription(test)))
            self.logger.debug(self.separator2)
            self.logger.debug("%s" % err)

    def _initTestResultDir(self):
        self.dirs = {}
        self.dirs['ws_report'] = self.builder.getWorkspace()
        self.dirs['ws_right'] = os.path.join(self.dirs['ws_report'],'right')
        self.dirs['ws_result'] = os.path.join(self.dirs['ws_report'],'%s-%s'%('result',self.builder.getProperty('starttime')))


    def _createDir(self,test):
        case_name = '%s.%s' %(type( test).__name__,  test._testMethodName)
        case_start_time = time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))
        if self.builder.getProperty('recording'):
            self.dirs['right'] = os.path.join(self.dirs['ws_right'],case_name)
            if not os.path.exists(self.dirs['right']):
                try:
                    os.makedirs(self.dirs['right'])
                except:
                    pass

        if self.builder.getProperty('testing'):
            foldername_with_timestamp = '%s-%s' % (case_name, case_start_time)
            self.dirs['right'] = os.path.join(self.dirs['ws_right'],case_name)
            self.dirs['all'] = os.path.join(os.path.join(self.dirs['ws_result'],'all'), foldername_with_timestamp)
            if not os.path.exists(self.dirs['all']):
                try:
                    os.makedirs(self.dirs['all'])
                except:
                    pass



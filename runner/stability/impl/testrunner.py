import sys,time
import unittest
from unittest import TestResult
from pubsub import pub
from stability.util.log import Logger
from testworker import testWorker
from builder import TestBuilder
from stability.util.log import Logger

class TestRunner(object):
    '''
    Class for loading test runner
    '''
    @staticmethod
    def getRunner(options=None):
        if not options is None:
            return PYTestRunner(options)
        else:
            return None

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
    
    @collectResult
    def startTest(self, test):
        TestResult.startTest(self, test)
        #need to add write and writln method for terminal output
        self.logger.debug(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
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

class PYTestRunner(object):
    '''
    Implement of text test runner
    '''
    def __init__(self, context=None):
        self.logger = Logger.getLogger()
        self.context = context

    def _makeResult(self):
        return _TestResult()

    def run(self, test):
        self.logger.debug('run the testsuite!!')
        #result output terminal
        result = self._makeResult()
        #test start time 
        startTime = time.time()
        #if test is instance of TestSuite:for t in test: i(result)
        #run test/testsuite
        test(result)
        #test stop time
        stopTime = time.time()
        #test duration
        timeTaken = stopTime - startTime
        #if not self.verbosity:
        #print all erros during test
        result.printErrors()
          #----------------
        self.logger.debug(result.separator2)
        #total case number has been ran
        run = result.testsRun
        self.logger.debug("Total ran %d test%s in %.3fs" % (run, run != 1 and "s" or "", timeTaken))
        #space line output
        #If test include failures or errors . special notification for failure and error
        if not result.wasSuccessful():
            self.logger.debug("FAILED (")
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                self.logger.debug("failures=%d" % failed)
            if errored:
                if failed:
                    self.logger.debug(", ")
                self.logger.debug("errors=%d" % errored)
            self.logger.debug(")")
        else:
            self.logger.debug("OK")
        return result

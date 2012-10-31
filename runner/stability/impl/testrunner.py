import sys,time,os,datetime
from unittest import TestResult
from testworker import testWorker
from builder import TestBuilder
from stability.util.log import Logger
from expectresult import ExpectResult
from listener import collectResult
from pubsub import pub
from resulthandler import ResultHandler
from uploader import ResultSender,Sender
class TestRunner(object):
    '''
    Class for loading test runner
    '''
    def __init__(self,option=None):
        self.logger = Logger.getLogger()
        self.options = option
        self.testResult = _TestResult()
        self.worker = testWorker(self.options)

    def runTest(self,test_suites):
        self.logger.debug('run the testsuite!!')
        startTime = datetime.datetime.now()
        if self.options['recording']:
            self.logger.debug('test mode: recording')
            for test in test_suites:
                self.worker.run(test,self.testResult)
            self.logger.debug('recording end')

        if self.options['testing']:
            for cycle in range(int(self.options['cycle'])):
                self.logger.debug('start cycle:/%s ' % (str(cycle),str(self.options['cycle']))
                for test in test_suites:
                    self.worker.run(test,self.testResult)
                self.logger.debug('end cycle:/%s ' % (str(cycle),str(self.options['cycle']))
        stopTime = datetime.datetime.now()
        self.logger.info('*****************************Test Summary*****************************')
        self.logger.info('Time Elapsed: %s' % (stopTime-startTime))
        self.logger.info('Success: %s' % self.testResult.success_count)
        self.logger.info('Failures: %s' % len(self.testResult.failures))
        self.logger.info('Errors: %s' % len(self.testResult.errors))
        pub.sendMessage('collectresult',sessionStatus='sessionstop')
        ResultSender.getInstance().queue.join()


class _TestResult(TestResult):
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, option=None,stream=None, descriptions=None, verbosity=None):
        TestResult.__init__(self)
        self.logger = Logger.getLogger()
        self.builder = TestBuilder.getBuilder()
        self._initTestResultDir()
        self.success_count = 0

    @collectResult
    def startTest(self, test):
        TestResult.startTest(self, test)
        self._createDir(test)
        self.logger.info('%s %s' % (self.case_start_time,str(test)))
    
    @collectResult
    def addSuccess(self,test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        self.logger.info('PASS')
            
    @collectResult
    def addFailure(self,test,err):
        TestResult.addFailure(self, test, err)
        self.logger.info('FAIL')

    @collectResult
    def addError(self, test, err):
        TestResult.addError(self, test, err)
        self.logger.info('ERROR')

    #@collectResult
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
            self.logger.info(self.separator1)
            self.logger.info("%s: %s" % (flavour,self.getDescription(test)))
            self.logger.info(self.separator2)
            self.logger.info("%s" % err)

    def _initTestResultDir(self):
        self.dirs = {}
        self.dirs['ws_report'] = self.builder.getWorkspace()
        self.dirs['ws_right'] = os.path.join(self.dirs['ws_report'],'right')
        self.dirs['ws_result'] = os.path.join(self.dirs['ws_report'],'%s-%s'%('result',self.builder.getProperty('starttime')))


    def _createDir(self,test):
        case_name = '%s.%s' %(type( test).__name__,  test._testMethodName)
        self.case_start_time = time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))
        if self.builder.getProperty('recording'):
            self.dirs['right'] = os.path.join(self.dirs['ws_right'],case_name)
            if not os.path.exists(self.dirs['right']):
                try:
                    os.makedirs(self.dirs['right'])
                except:
                    pass

        if self.builder.getProperty('testing'):
            foldername_with_timestamp = '%s-%s' % (case_name, self.case_start_time)
            self.dirs['right'] = os.path.join(self.dirs['ws_right'],case_name)
            self.dirs['all'] = os.path.join(os.path.join(self.dirs['ws_result'],'all'), foldername_with_timestamp)
            if not os.path.exists(self.dirs['all']):
                try:
                    os.makedirs(self.dirs['all'])
                except:
                    pass



'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import sys,time,os,datetime,traceback
from unittest import TestResult
from testworker import testWorker
from builder import TestBuilder
from stability.util.log import Logger
from expectresult import ExpectResult
from listener import collectResult
from pubsub import pub
from uploader import ResultSender,Sender

class TestRunner(object):
    '''
    Class for controling the test suites.
    '''
    def __init__(self,option=None):
        self.logger = Logger.getLogger()
        self.options = option
        self.testResult = _TestResult()
        self.worker = testWorker(self.options)

    def runTest(self,test_suites):
        '''
        Start the test sequences.
        '''
        self.logger.debug('run the testsuite...')
        startTime = datetime.datetime.now()
        if self.options['testing']:
            for cycle in range(int(self.options['cycle'])):
                self.logger.info('start cycle: %s/%s' % (str(cycle+1),str(self.options['cycle'])))
                for test in test_suites:
                    self.worker.run(test,self.testResult)
                self.logger.info('end cycle: %s/%s' % (str(cycle+1),str(self.options['cycle'])))
        stopTime = datetime.datetime.now()
        self.logger.info('*****************************Test Summary*****************************')
        self.logger.info('Time Elapsed: %s' % (stopTime-startTime))
        self.logger.info('Success: %s' % self.testResult.success_count)
        self.logger.info('Failures: %s' % len(self.testResult.failures))
        self.logger.info('Errors: %s' % len(self.testResult.errors))
        if self.options['uploadresult']:
            pub.sendMessage('collectresult',sessionStatus='sessionstop')
            ResultSender.getInstance().queue.join()


class _TestResult(TestResult):
    '''
    Class for output test case result.
    '''
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
        sys.stderr.write('%s %s ' % (self.case_start_time,str(test)))
        self.logger.debug('%s %s ' % (self.case_start_time,str(test)))

    @collectResult
    def addSuccess(self,test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        sys.stderr.write('ok\n')
        self.logger.debug('PASS')
            
    @collectResult
    def addFailure(self,test,err):
        TestResult.addFailure(self, test, err)
        sys.stderr.write('F\n')
        self.logger.debug('FAIL')

    @collectResult
    def addError(self, test, err):
        TestResult.addError(self, test, err)
        sys.stderr.write('E\n')
        self.logger.debug('ERROR')
        self.logger.debug(self._trace_to_string((err,test)))

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
        self.dirs['ws'] = self.builder.getWorkspace()
        self.dirs['ws_report'] = os.path.join(self.dirs['ws'],'report')
        #TODO
        #self.dirs['ws_right'] = os.path.join(self.dirs['ws'],'%s%s%s' % ('testcase',os.sep,'cases'))
        if self.builder.getProperty('product'):
            self.dirs['ws_right'] = os.path.join(self.dirs['ws'],'%s%s%s' % (self.builder.getProperty('product'),os.sep,'cases'))            
        else:
            self.dirs['ws_right'] = os.path.join(self.dirs['ws'],'%s%s%s' % ('testcase',os.sep,'cases'))
        self.dirs['ws_result'] = os.path.join(self.dirs['ws_report'],'%s-%s' % ('result',self.builder.getProperty('starttime')))

    def _createDir(self,test):
        class_name = test.__module__.split('.')[2]
        case_name = '%s.%s' %(type( test).__name__,  test._testMethodName)
        self.case_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        ###if self.builder.getProperty('recording'):
        ###    self.dirs['right'] = os.path.join(self.dirs['ws_right'],case_name)
        ###    if not os.path.exists(self.dirs['right']):
        ###        try:
        ###            os.makedirs(self.dirs['right'])
        ###        except:
        ###            pass
        if self.builder.getProperty('testing'):
            foldername_with_timestamp = '%s-%s' % (case_name, self.case_start_time)
            ###self.dirs['right'] = os.path.join(self.dirs['ws_right'],case_name)
            self.dirs['right'] = os.path.join(self.dirs['ws_right'],'%s.%s'%(class_name,case_name))
            self.dirs['all'] = os.path.join(os.path.join(self.dirs['ws_result'],'all'), foldername_with_timestamp)
            if not os.path.exists(self.dirs['all']):
                try:
                    os.makedirs(self.dirs['all'])
                except:
                    pass

    def _trace_to_string(self,traceinfo):
        '''Converts err,test into a string as trace log.'''
        if not isinstance(traceinfo,tuple):
            return traceinfo
        exctype, value, tb = traceinfo[0]
        # Skip test runner traceback levels
        while tb and  ResultSender._is_relevant_tb_level(tb):
            tb = tb.tb_next
        if exctype is traceinfo[1].failureException:
            # Skip assert*() traceback levels
            length =  ResultSender._count_relevant_tb_levels(tb)
            return ''.join(traceback.format_exception(exctype, value, tb, length))
        return ''.join(traceback.format_exception(exctype, value, tb))

    def _is_relevant_tb_level(self,tb):
            return '__unittest' in tb.tb_frame.f_globals

    def _count_relevant_tb_levels(self,tb):
            length = 0
            while tb and not ResultSender._is_relevant_tb_level(tb):
                length += 1
                tb = tb.tb_next
            return length

#!/usr/bin/env python  
#coding: utf-8

'''
Module provides the function to output test result.
@version: 1.0
@author: borqsat
@see: null
'''

import os,time,sys
from os.path import join,abspath,dirname
from ps import Topics,emit
from unittest import TestResult
import constants
from serialize import Serializer
import traceback
import variables
import shutil, errno
#WORK_SPACE = dirname(dirname(dirname(abspath(__file__))))

def _clsname(cls):
    return cls.__module__ + "." + cls.__name__

def _casename(test):
    return '%s%s%s' % (type(test).__name__,'.',test._testMethodName)

def _time():
    return time.strftime(variables.TIME_STAMP_FORMAT, time.localtime(time.time()))

def _is_relevant_tb_level(tb):
    return '__unittest' in tb.tb_frame.f_globals


def _count_relevant_tb_levels(tb):
    length = 0
    while tb and not _is_relevant_tb_level(tb):
        length += 1
        tb = tb.tb_next
    return length

def _trace_to_string(traceinfo):
    '''Converts err,test into a string as trace log.'''
    if not isinstance(traceinfo,tuple):
        return traceinfo
    exctype, value, tb = traceinfo[0]
    # Skip test runner traceback levels
    while tb and  _is_relevant_tb_level(tb):
        tb = tb.tb_next
    if exctype is traceinfo[1].failureException:
        # Skip assert*() traceback levels
        length =  _count_relevant_tb_levels(tb)
        return ''.join(traceback.format_exception(exctype, value, tb, length))
    return ''.join(traceback.format_exception(exctype, value, tb))

def _mkdir(path):
    '''create dir as path'''
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def _copy(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def collect_result(func):
    '''
    Decorator of function. It publishes messages to some topic
    '''
    def wrap(*args, **argkw):
        func(*args, **argkw)

        if func.__name__ == 'startTest':
            emit(Topics.UPLOAD, data={'directory':args[0].localpath['ws_result']})

        elif func.__name__ == 'addSuccess':
            fpath = join(args[0].localpath['ws_testcase'],variables.RESULT_FILE_NAME)
            Serializer.serialize(file_path=fpath, data={'result':'pass','endtime':_time(),'traceinfo':'N/A'})
            _copy(args[0].localpath['ws_testcase'],join(args[0].localpath['ws_result_pass'],'%s_%s' % (args[0]._case_name,args[0]._case_start_time)))
            #Serializer.serialize(file_path=fpath, data={'result':'pass','time':_time(),'traceinfo':'N/A'})

        elif func.__name__ == 'addFailure':
            log_dest = _mkdir(join(args[0].localpath['ws_testcase'],'log'))
            snapshots = args[0].localpath['ws_testcase_right']
            device = getattr(args[1],'device',None)
            if device: device.catchLog(log_dest)
            #move right snapshots to all/case
            expect_result = getattr(device,'expect_result',None)
            if expect_result:
                origin = expect_result.getFullCurrentCheckPointPath()
                dirs,filename = os.path.split(origin)
                target = join(args[0].localpath['ws_testcase'],'%s%s'%('origin_',filename))
                shutil.copy(origin,target)
            fpath = join(args[0].localpath['ws_testcase'],variables.RESULT_FILE_NAME)
            traceinfo = _trace_to_string((args[2],args[1]))
            Serializer.serialize(file_path=fpath, data={'result':'fail','endtime':_time(),'trace':traceinfo})
            _copy(args[0].localpath['ws_testcase'],join(args[0].localpath['ws_result_fail'],'%s_%s' % (args[0]._case_name,args[0]._case_start_time)))
            #Serializer.serialize(file_path=fpath, data={'result':'fail','time':_time(),'trace':traceinfo})

        elif func.__name__ == 'addError':
            log_dest = _mkdir(join(args[0].localpath['ws_testcase'],'log'))
            snapshots = args[0].localpath['ws_testcase_right']
            device = getattr(args[1],'device',None)
            if device: device.catchLog(log_dest)
            fpath = join(args[0].localpath['ws_testcase'],variables.RESULT_FILE_NAME)
            traceinfo = _trace_to_string((args[2],args[1]))
            Serializer.serialize(file_path=fpath, data={'result':'error','endtime':_time(),'trace':traceinfo})
            _copy(args[0].localpath['ws_testcase'],join(args[0].localpath['ws_result_error'],'%s_%s' % (args[0]._case_name,args[0]._case_start_time)))
            #Serializer.serialize(file_path=fpath, data={'result':'error','time':_time(),'trace':traceinfo})
        elif func.__name__ == 'stopTest':
            emit(Topics.UPLOAD, data={'directory':args[0].localpath['ws_result']})

        return func
    return wrap

class TestResultImpl(TestResult):
    '''
    Holder for test result information. Each instance holds the total number of tests run, and collections of failures and errors that occurred among those test runs. The collections contain tuples of (testcase, exceptioninfo), where exceptioninfo is the   formatted traceback of the error that occurred.
    '''
    @property
    def options(self):
        return self._options

    @property
    def localpath(self):
        return self._local_storage

    def __init__(self, option):
        TestResult.__init__(self)
        self._options = option
        self._case_name = None
        self._case_start_time = None
        self._failure = None
        self._error = None
        self._pass = None
        self._success_count = 0
        self._local_storage = {}
        session_start_time = _time()
        ws = variables.WORK_SPACE
        ws_report = join(ws,variables.REPORT_DIR_NAME)
        ws_result = join(ws_report,'%s@%s' % (self._options['product'], session_start_time))
        self._local_storage['ws'] = ws
        #self._local_storage['session_start_time'] = ws
        self._local_storage['ws_report'] = _mkdir(ws_report)
        self._local_storage['ws_result'] = _mkdir(ws_result)
        self._local_storage['ws_result_all'] = _mkdir(join(ws_result,'all'))
        self._local_storage['ws_result_pass'] = _mkdir(join(ws_result,'pass'))
        self._local_storage['ws_result_fail'] = _mkdir(join(ws_result,'fail'))
        self._local_storage['ws_result_error'] = _mkdir(join(ws_result,'error'))

    @collect_result    
    def startTest(self, test):
        TestResult.startTest(self, test)
        self._error, self._failure = None, None
        self._case_name = _casename(test)
        self._case_start_time = _time()
        self._local_storage['testcase_starttime'] = self._case_start_time
        self._local_storage['ws_testcase'] = _mkdir(join(self._local_storage['ws_result_all'], '%s@%s' % (self._case_name,self._case_start_time)))
        self._local_storage['ws_testcase_right'] = _mkdir(join(self._local_storage['ws'],self._options['product'],'cases','%s.%s'%(test.__module__.split('.')[2],self._case_name)))
        sys.stderr.write('%s %s'%(self._case_start_time,str(test)))
        import time
        time.sleep(10)

    @collect_result
    def addSuccess(self, test):
        TestResult.addSuccess(self, test)
        self._success_count += 1

    @collect_result
    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        self._failure = err
        #print test.id()

    @collect_result 
    def addError(self, test, err):
        TestResult.addError(self, test, err)
        self._error = err

    @collect_result
    def stopTest(self, test):
        TestResult.stopTest(self, test)
        end_time = _time()
        if self._error:
            sys.stderr.write(' error\n')
        elif self._failure:
            sys.stderr.write(' fail\n')
        else:
            sys.stderr.write(' pass\n')

class TestInfo(object):

    '''
    Used to represent a formated result.
    '''

    def __init__(self, test, time):
        (self._class, self._method) = test.id().rsplit(".", 1)
        self._time = time
        self._error = None
        self._failure = None

    @staticmethod
    def create_success(test, time):
        """Create a _TestInfo instance for a successful test."""
        return _TestInfo(test, time)

    @staticmethod
    def create_failure(test, time, failure):
        """Create a _TestInfo instance for a failed test."""
        info = _TestInfo(test, time)
        info._failure = failure
        return info

    @staticmethod
    def create_error(test, time, error):
        """Create a _TestInfo instance for an erroneous test."""
        info = _TestInfo(test, time)
        info._error = error
        return info

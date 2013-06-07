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
from ps import Topics
from ps import Message
from ps import on,emit
from unittest import TestResult
import constants
WORK_SPACE = dirname(dirname(dirname(abspath(__file__))))

def collect_result(func):
    '''
    Decorator of function. It publishes messages to some topic
    '''
    def wrap(*args, **argkw):
        func(*args, **argkw)
        #content = (func.__name__,args)
        if func.__name__ == '__init__':
            #pub session start message  
            pass
        elif func.__name__ == 'addStart':
            #request_file_path = os.path.join(args[0].local_storage['ws_testcase'],'casestart.req')
            #dir_path = ''
            sessionstarttime = args[0].localpath['session_start_time']
            #Message(topic= Topics.TOPIC_RESULT, data = {'sessionstarttime': args[0]['testcase_starttime'],'casename':''})()
            ##pub case start message
            pass
        elif func.__name__ == 'addSuccess':
            #request_file_path = os.path.join(args[0].local_storage['ws_testcase'],'pass.req')
            #dir_path = ''
            #Message(topic=Topics.TOPIC_RESULT, tag='caseresult', data = {'casename':case_name,'result':'pass'})()
            pass
        elif func.__name__ == 'addFailure':
            #request_file_path = os.path.join(args[0].local_storage['ws_testcase'],'failure.req')
            #dir_path = ''
            #Message(topic=Topics.TOPIC_RESULT, tag='caseresult' , data = {'casename':case_name,'result':'fail'})()
            pass
        elif func.__name__ == 'addError':
            #request_file_path = os.path.join(args[0].local_storage['ws_testcase'],'error.req')
            #dir_path = ''
            #Message(topic=Topics.TOPIC_RESULT, tag='caseresult', data = {'casename':case_name,'result':'fail'})()
            pass
        elif func.__name__ == 'stopTest':
            #request_file_path = os.path.join(args[0].local_storage['ws_testcase'],'error.req')
            #dir_path = ''
            #Message(topic=Topics.TOPIC_RESULT, tag='caseresult', data = {'casename':case_name,'result':'fail'})()
            #catch useful log
            #pub case result message
            pass
        return func
    return wrap


def log(func):
    '''
    Decorator of function. Pub the message to catch device log.
    '''
    def wrap(*args, **argkw):
        func(*args, **argkw)
        if func.__name__ == 'addFailure':
            log_dest = args[0].localpath['ws_testcase']
            snapshots = args[0].localpath['ws_testcase_right']
            device = getattr(args[1],'device')
            device.catchLog(log_dest)
            #emit(topic='log', data={'result':'fail','dest':log_dest,'snapshots':snapshots})
            #Message(topic='log',data={'result':'fail','dest':log_dest,'snapshots':snapshots})()
        elif func.__name__ == 'addError':
            log_dest = args[0].localpath['ws_testcase']
            snapshots = args[0].localpath['ws_testcase_right']
            device = getattr(args[1],'device')
            device.catchLog(log_dest)
            #emit(topic='log', data={'result':'error','dest':log_dest,'snapshots':snapshots})
            #Message(topic='log',data={'result':'error','dest':log_dest,'snapshots':snapshots})()
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
        ws = dirname(dirname(dirname(abspath(__file__))))
        ws_report = join(ws,'report')
        ws_result = join(ws_report,'%s-%s' % (self._options['product'], session_start_time))
        self._local_storage['ws'] = ws
        self._local_storage['session_start_time'] = ws
        self._local_storage['ws_report'] = ws_report
        self._local_storage['ws_result'] = ws_result
        if not os.path.exists(ws_report):
            os.makedirs(ws_report)
        if not os.path.exists(ws_result):
            os.makedirs(ws_result)
        
    @collect_result    
    def startTest(self, test):
        TestResult.startTest(self, test)
        self._error, self._failure = None, None
        self._case_name = _casename(test)
        self._case_start_time = _time()
        self._local_storage['testcase_starttime'] = self._case_start_time
        self._local_storage['ws_testcase'] = join(self._local_storage['ws_result'], 'all', '%s-%s' % (self._case_name,self._case_start_time))
        if not os.path.exists(self._local_storage['ws_testcase']):
            os.makedirs(self._local_storage['ws_testcase'])
        self._local_storage['ws_testcase_right'] = join(self._local_storage['ws'],self._options['product'],'cases','%s.%s'%(test.__module__.split('.')[2],self._case_name))
        sys.stderr.write('%s %s'%(self._case_start_time,str(test)))

    def addSuccess(self, test):
        TestResult.addSuccess(self, test)
        self._success_count += 1

    @log
    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        self._failure = err
        print test.id()

    @log  
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

def _clsname(cls):
    return cls.__module__ + "." + cls.__name__

def _casename(test):
    return '%s%s%s' % (type(test).__name__,'.',test._testMethodName)

def _time():
    return time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))
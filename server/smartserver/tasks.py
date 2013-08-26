#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from .worker import worker as w
from .v0.impl.dbstore import store
from .v0 import sendmail 


@w.task(ignore_result=True)
def ws_del_session(sid):
    '''
    Delete FS according to the sid by using worker task
    '''
    store.del_session(sid)


@w.task(ignore_result=True)
def ws_del_group(gid):
    '''
    Delete FS and results according to gid by using worker task
    '''
    store.del_group(gid)


@w.task(ignore_result=True)
def ws_del_dirty():
    '''
    Scheduled task to clear dirty FS.
    '''
    store.del_dirty()


@w.task(ignore_result=True)
def ws_check_fs(fid):
    store.check_fs(fid)


@w.task(ignore_result=True)
def ws_validate_session_endtime():
    store.validate_session_endtime()


@w.task(ignore_result=True)
def ws_active_testsession(sid):
    store.active_testsession(sid)


@w.task(ignore_result=True)
def ws_validate_testcase_endtime():
    store.validate_testcase_endtime()


@w.task(ignore_result=True)
def ws_update_testsession_summary(sid):
    store.updateTestsessionSummary(sid)

@w.task(ignore_result=True)
def ws_validate_token_expiretime():
    store.validate_token_expiretime()

@w.task(ignore_result=True)
def ws_send_mail_to_user(link, address):
    sendmail.sendReportMail(link, address)


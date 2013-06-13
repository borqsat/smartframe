from __future__ import absolute_import

from .worker import worker as w

from .v0.impl.dbstore import store

@w.task
def ws_del_session(sid):
    '''
    Delete FS according to the sid by using worker task
    '''
    store.del_session(sid)

@w.task
def ws_del_group(gid):
    '''
    Delete FS and results according to gid by using worker task
    '''
    store.del_group(gid)

@w.task
def ws_del_dirty():
    '''
    Scheduled task to clear dirty FS.
    '''
    store.del_dirty()

@w.task
def ws_check_fs(fid):
    store.check_fs(fid)

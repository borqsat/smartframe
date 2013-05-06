from __future__ import absolute_import

from .worker import worker as w

from .v0.impl.dbstore import store
from bson.objectid import ObjectId

@w.task
def add(x, y):
    return x + y


@w.task
def mul(x, y):
    return x * y


@w.task
def xsum(numbers):
    return sum(numbers)

@w.task
def delSessionFs(sid):
    '''
    Delete FS according to the sid by using worker task
    '''
    caseresult = store._db['testresults']
    crs = caseresult.find({'sid':sid, 'result':'fail'})
    for record in crs:
        if 'snapshots' in record:
            snapshots = record['snapshots']
            for snap in snapshots: store.deletefile(snap['fid'])
            
        if 'checksnap' in record:
            checksnap = record['checksnap']
            store.deletefile(checksnap['fid'])
            store.deletefile(record['log'])

@w.task
def delGroupFs(gid):
    '''
    Delete FS and results according to gid by using worker task
    '''

@w.task
def delDirtyFs():
    '''
    Scheduled task to clear dirty FS.
    '''

from __future__ import absolute_import

from smartworker.worker import worker as w

import os 
import time

from smartserver.v0.impl.dbstore import store

@w.task
def add(x, y):
    time.sleep(20)
    return x + y


@w.task
def mul(x, y):
    return x * y

@w.task
def minus(x, y):
    return x - y

@w.task
def xsum(numbers):
    return sum(numbers)


@w.task
def touchfile():
	os.system('touch /tmp/%s'%time.time())


@w.task
def delSessionFs(sid):
    '''Delete session resources in stand-alone worker
    '''
    caseresult = store._db['testresults']
    caseresult.remove({'sid': sid})
    cases = caseresult.find({'sid': sid, 'result': 'fail'})
    for record in cases:
        if 'snapshots' in record:
            snapshots = record['snapshots']
            for snap in snapshots: self.deletefile(snap['fid'])
            
        if 'checksnap' in record:
            checksnap = record['checksnap']
            self.deletefile(checksnap['fid'])
        if 'checksnap' in record:
            log = record['log']
            self.deletefile(log)

@w.task
def delGroupFs(gid):
    '''Delete all relative fs of gid'''

@w.task
def clearDirtyFs():
    '''Clear all dirty fs
    '''



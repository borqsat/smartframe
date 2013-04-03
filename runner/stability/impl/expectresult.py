'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import time, sys, os, shutil, datetime, string,re
from stability.util.log import Logger

class ExpectResult:
    '''Class for maintaining the test resources'''
    def __init__(self,path=None):
        self.cusor = -1
        self.resultPath = path

    def getCurrentPath(self,name=None):
        '''Get the path of current checkpoint'''
        tag = '.png'
        if name:
            check_point_name = '%s'%name
        else:
            self.cusor = self.cusor + 1
            check_point_name = self.__basename(str(self.cusor))['checkpoint']
        check_point_path = '%s%s' % (os.path.join(self.resultPath,check_point_name),tag)
        self.currentCheckPoint = check_point_path
        assert os.path.exists(check_point_path), '%s %s' % ('No such file:',check_point_path)
        return check_point_path

    def getCurrentCheckPoint(self):
        '''Get the current checkpoint name'''
        return self.currentCheckPoint

    def getCurrentCheckPointParent(self):
        '''Get the full snapshot path of current checkpoint'''
        full_path = ''
        try:
            dirs,filename = os.path.split(self.currentCheckPoint)
            name,ext = os.path.splitext(filename)
            assert os.path.exists(dirs) , '%s %s' % ('No such directory:',dirs)
            reg = '%s..+%s' % (name,ext)
            full_name = self._getFullSnapshot(dirs,reg)
            full_path = '%s%s%s' % (dirs,os.sep,full_name)
        finally:
            return full_path

    def _getFullSnapshot(self,filedir,substr):
        '''Get snapshot path'''
        pattern = re.compile(substr)
        if os.path.exists(filedir):
            for f in os.listdir(filedir):
                hit = pattern.search(f)
                if hit:
                    return f

    def __basename(self, name):
        '''Get base path'''
        names = {}
        names['snapshot'] = '%s.wait.snapshot.png' % name
        names['checkpoint'] = '%s.wait.checkpoint.png' % name
        names['ocr'] = '%s.ocr.txt' % name
        return names

'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import time, sys, os, shutil, datetime, string,re
from stability.util.log import Logger

class ExpectResult:
    def __init__(self,path=None):
        self.cusor = -1
        self.resultPath = path


    def getCurrentPath(self,name=None):
        tag = '.png'
        if name:
            check_point_name = '%s'%name
        else:
            self.cusor = self.cusor + 1
            check_point_name = self.basename(str(self.cusor))['checkpoint']            
        check_point_path = '%s%s' % (os.path.join(self.resultPath,check_point_name),tag)
        self.currentCheckPoint = check_point_path
        return check_point_path

    def getCurrentCheckPoint(self):
        return self.currentCheckPoint

    def getCurrentCheckPointParent(self):
        dirs,filename = os.path.split(self.currentCheckPoint)
        name,ext = os.path.splitext(filename)
        reg = '%s..+%s' % (name,ext)
        full_name = self._getFullSnapshot(dirs,reg)
        full_path = '%s%s%s' % (dirs,os.sep,full_name)
        return full_path

    def _getFullSnapshot(self,filedir,substr):
        pattern = re.compile(substr)
        for f in os.listdir(filedir):
            hit = pattern.search(f)
            if hit:
                return f 

    def basename(self, name):
        names = {}
        names['snapshot'] = '%s.wait.snapshot.png' % name
        names['checkpoint'] = '%s.wait.checkpoint.png' % name
        names['ocr'] = '%s.ocr.txt' % name
        return names

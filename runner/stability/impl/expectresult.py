'''
Module for maintaining the collection of each test case snapshot.
@version: 1.0
@author: borqsat
@see: null
'''

import time, sys, os, shutil, datetime, string,re
from stability.util.log import Logger

class ExpectResult:
    '''
    Class for maintaining the collection of each test case snapshot.
    '''
    def __init__(self,path=None):
        '''
        Init instance of ExpectResult.
        '''
        self.cusor = -1
        self.resultPath = path

    def getCurrentPath(self,name=None):
        '''
        Return the file path by name.
        @rtype: string
        @return: the file path
        '''
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
        '''
        Return the current check point snapshot path .
        @rtype: string
        @return: the file path
        '''
        return self.currentCheckPoint

    def getCurrentCheckPointParent(self):
        '''
        Return the full snapshot path of current check point .
        @rtype: string
        @return: the file path
        '''
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
        '''
        Return the full snapshot path of current check point .
        '''
        pattern = re.compile(substr)
        if os.path.exists(filedir):
            for f in os.listdir(filedir):
                hit = pattern.search(f)
                if hit:
                    return f

    def __basename(self, name):
        '''
        Generate snapshot name.
        '''
        names = {}
        names['snapshot'] = '%s.wait.snapshot.png' % name
        names['checkpoint'] = '%s.wait.checkpoint.png' % name
        names['ocr'] = '%s.ocr.txt' % name
        return names

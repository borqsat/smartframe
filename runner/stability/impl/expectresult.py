#!/usr/bin/env python
import time, sys, os, shutil, datetime, string
from stability.util.log import Logger

class ExpectResultDemo:
    '''Provides the access ability to the expectResult data store'''
    def __init__(self,casename=None,basedir=None):
        self.workdir = basedir
        self.caseName = casename
        pass

    def init(self, case):
        self.cursor = -1
        foldername = '%s.%s' %(type(case).__name__, case._testMethodName)
        self.caseResdir = os.join(self.workdir, foldername) 
        self.expReslist = []
    
    def getCurrency(self):
        self.cursor += 1
        if self.cursor < len(self.expReslist):
            return self.expReslist[self.cursor]
        else:
            return None

class ExpectResult:
    def __init__(self,path=None):
        self.cusor = -1
        self.resultPath = path


    def getCurrentPath(self):
        self.cusor = self.cusor + 1
        check_point_name = self.basename(str(self.cusor))['checkpoint']
        check_point_path = os.path.join(self.resultPath,check_point_name)
        return check_point_path

    def basename(self, name):
        names = {}
        names['snapshot'] = '%s.wait.snapshot.png' % name
        names['checkpoint'] = '%s.wait.checkpoint.png' % name
        names['ocr'] = '%s.ocr.txt' % name
        return names

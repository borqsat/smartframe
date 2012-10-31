#!/usr/bin/env python
import time, sys, os, shutil, datetime, string
from stability.util.log import Logger

class ExpectResult:
    def __init__(self,path=None):
        self.cusor = -1
        self.resultPath = path


    def getCurrentPath(self,name=None):
        if name:
            check_point_name = '%s'%name
        else:
            self.cusor = self.cusor + 1
            check_point_name = self.basename(str(self.cusor))['checkpoint']            
        check_point_path = os.path.join(self.resultPath,check_point_name)
        self.currentCheckPoint = check_point_path
        return check_point_path

    def getCurrentCheckPoint(self):
        return self.currentCheckPoint

    def basename(self, name):
        names = {}
        names['snapshot'] = '%s.wait.snapshot.png' % name
        names['checkpoint'] = '%s.wait.checkpoint.png' % name
        names['ocr'] = '%s.ocr.txt' % name
        return names

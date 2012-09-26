#!/usr/bin/env python
import time, sys, os, shutil, datetime, string
from stability.util.log import Logger

__DEFAULT_PATH = {'right':'./report/right',
                  'all':'./report/result-tmp/all',
                  'fail':'./report/result-tmp/fail',
                  'error':'./report/result-tmp/error'
                 }

class store:
    """Provides the access ability to the case result data store"""

    def __init__(self, context=None, case=None):    
        self.logger = Logger.getLogger()    
        self.logger.debug('init store instance!')
        if (context is None) or (case is None):
            self.outdirs = __DEFAULT_PATH
            self.istesting = True
        else:
            self.logger.debug('init store for testcase!!!')
            self.workspace = context.getWorkspace()
            self.istesting = context.isTesting()
            self.starttime = context.getStartTime()
            self.case = case
            self.outdirs = self.__createOutDirs()


    def basename(self, name):
        names = {}
        names['snapshot'] = '%s.snapshot.png' % name
        names['checkpoint'] = '%s.checkpoint.png' % name
        names['ocr'] = '%s.ocr.txt' % name
        return names
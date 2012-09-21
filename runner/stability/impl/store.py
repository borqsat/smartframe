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

    def __createOutDirs(self):
        dirs={}
        foldername = '%s.%s' %(type(self.case).__name__, self.case._testMethodName)
        dirs['right'] = os.path.join(self.workspace, 'right', foldername)
        #if self.istesting:
        report_folder_name = ('%s-%s'%('result',self.starttime))
        workspace_report = os.path.join(self.workspace,report_folder_name)
        foldername_with_timestamp = '%s-%s' % (foldername, self.case.starttime)
        dirs['all'] = os.path.join(workspace_report, 'all', foldername_with_timestamp)
        dirs['fail'] = os.path.join(workspace_report, 'fail', foldername_with_timestamp)
        dirs['error'] = os.path.join(workspace_report, 'error', foldername_with_timestamp)

        for k in ['right','all']:
            try:
                self.logger.debug(k + ':'+ dirs[k])
                os.makedirs(dirs[k])
            except:
                pass
        return dirs

    def basename(self, name):      
        names = {}
        names['snapshot'] = '%s.snapshot.png' % name
        names['checkpoint'] = '%s.checkpoint.png' % name
        names['ocr'] = '%s.ocr.txt' % name
        return names

    def getWorkDir(self):
        if self.istesting:
            return self.outdirs['all']
        else:
            return self.outdirs['right']

    def getRightDir(self):
        if self.istesting:
            return self.outdirs['right']

    def getFailDir(self):
        if self.istesting:
            return self.outdirs['fail']

    def getErrorDir(self):
        if self.istesting:
            return self.outdirs['error']
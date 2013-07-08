#!/usr/bin/env python  
#coding: utf-8
'''
Module for maintaining the collection of each test case resources. Like all chekpoints...
@version: 1.0
@author: borqsat
@see: null
'''
from os.path import join
import os,re

class ExpectResult:
    '''
    Class for maintaining the collection of each test case resources. Like all chekpoints...
    '''
    def __init__(self,resource_path):
        '''
        Init instance of ExpectResult.
        '''
        self._cusor = -1
        self._rpath = resource_path

    def getCurrentCheckPointPath(self,name=None):
        '''
        get the current check ponit snapshot file path
        @rtype: string
        @return: path of current check point
        '''
        self.current_check_point = join(self._rpath,name)
        assert os.path.exists(self.current_check_point), '%s %s' % ('No such file:',self.current_check_point)
        return self.current_check_point

    def getExpectResultPath(self,name=None):
        '''
        get the current expected snapshot file path
        @rtype: string
        @return: path of current expected check point
        '''
        pass

    def getFullCurrentCheckPointPath(self):
        '''
        get the current expected snapshot full image file path
        @rtype: string
        @return: path of current check point full image file path
        '''
        sub_full_path = ''
        try:
            dirs,filename = os.path.split(self.current_check_point)
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
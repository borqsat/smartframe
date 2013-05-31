#!/usr/bin/env python  
#coding: utf-8
'''
Module for maintaining the collection of each test case resources. Like all chekpoints...
@version: 1.0
@author: borqsat
@see: null
'''
from os.path import join

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
        return join(self._rpath,name)

    def getExpectResultPath(self,name=None):
        '''
        get the current expected snapshot file path
        @rtype: string
        @return: path of current expected check point
        '''
        pass

    def getFullExpectedResultPath(self):
        '''
        get the current expected snapshot full image file path
        @rtype: string
        @return: path of current check point full image file path
        '''
        pass

#!/usr/bin/env python  
#coding: utf-8

'''
Tizen device implemention.
@version: 1.0
@author: borqsat
@see: null
'''

from device import BaseDevice

class Device(BaseDevice):
    def __init__(self):
        '''Tizen Device for Tizen platform'''
        super(TizenDevice,self).__init__()
        self.serial = ''
        self.impl = None

    def getConnect(self):
        '''Connected to real Tizen Device'''
        self.impl = None

    def resumeConnect(self):
        '''Re-connected to real Android Device'''
        self.impl = None

    def getSerialId(self):
        pass
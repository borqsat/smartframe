#!/usr/bin/env python  
#coding: utf-8
'''
Module provides the function to maintain collecion of availiable devices. and the class represent a device instance.
@version: 1.0
@author: borqsat
@see: null
'''

import time,sys,os,threading
from android import Device

class DeviceManager(object):
    '''DeviceManager maintains collecion of availiable devices'''
    _instance = None
    _mutex = threading.Lock()

    def __init__(self):
        '''Init DeviceManager Instance.'''
        self._devices = list()

    @staticmethod
    def getInstance(context=None):
        '''Get single instance of DeviceManager'''
        if(DeviceManager._instance == None):
            DeviceManager._mutex.acquire()
            if(DeviceManager._instance == None):
                DeviceManager._instance = DeviceManager()
            else:
                pass
            DeviceManager._mutex.release()
        else:
            pass

        if not context is None:
            DeviceManager._instance.setContext(context)
        return DeviceManager._instance

    def setContext(self, context=None):
        '''set application context if exists'''
        self.platform = context
        #import importlib
        #android = __import__(self.platform)
        #print android
        #a = __import__('android')
        #print '>>>>>>>>>>>>>>>>>>>>???????????'
        #print self.platform
        #self.m = __import__('.%s'%self.platform, fromlist=['Device'])
        
    #@device
    def getDevice(self):
        '''Get instance of device '''
        #device = getattr(self.platform, 'Device')
        self._device = Device()
        self._device.getConnect()
        self._devices.append(self._device)
        return self._device

    def getDevices(self):
        '''
        Get the device collection list.
        '''
        return self._devices


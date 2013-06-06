#!/usr/bin/env python  
#coding: utf-8
'''
Module provides the function to maintain collecion of availiable devices. and the class represent a device instance.
@version: 1.0
@author: borqsat
@see: null
'''

import time,sys,os,threading
#from android import Device

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
        
    def getDevice(self):
        '''
        Get instance of target device.
        rtype :the subclass of BaseDevice
        rparam :the subclass instance  of BaseDevice
        Exception: Throw exception when device init failed or recover failed.
        '''
        moudle = __import__('stability.impl.%s' % self.platform, fromlist=['Device'])
        device = getattr(moudle, 'Device')
        try:
            self._device = device()
            if not self._device.available():
                self._device.recover()
        except DeviceInitException,e1:
            print e1
        except DeviceRecoverException,e2:
            print e2
        self._devices.append(self._device)
        return self._device

    def getDevices(self):
        '''
        Get the device collection list.
        '''
        return self._devices

class BaseDevice(object):
    '''
    Abstract class for respresenting device instance ability.
    The subclass of BaseDevice should extends from this class. and implement available() 
    recover() method. and provide the ability to interacte with device. E.g: touch , press.
    takeSnapshot() 
    '''

    def __init__(self):
        '''
        Abstract class for device.
        Exception: throw DeviceInitException if device init failed.
        '''
        pass

    def __call__(self,*argv,**kwags):
        return self

    def available(self):
        '''
        check the device status.
        rtype boolean 
        rparam return True if device avaiable. False if unavailable.
        '''
        pass

    def recover(self):
        '''
        Recover the device when device unavailable.
        rtype boolean 
        rparam return True if device avaiable. False if unavailable.
        Exception: Throw DeviceRecoverException if recover failed.
        '''
        pass

    def touch(self,*argv, **kwargs):
        '''
        Perform a touch event on the touch point or on the screen region.
        The touch point specified by type to the screen location specified by x and y. or image or
        a description of screen element.
        If the screen region want to touch not found in the current screen snapshot should throw exception.
        '''
        pass

    def takeSnapshot(self,*argv, **kwargs):
        pass

class DeviceRecoverException(Exception):
    '''
    Raised when attempt to recover a device failed.
    '''
    def __init__(self, value):
        Exception.__init__(self, value)
        self.value = value

    def __str__(self):
        return repr(self.value)

class DeviceInitException(Exception):
    '''
    Raised when attempt to init a device failed.
    '''
    def __init__(self, value):
        Exception.__init__(self, value)
        self.value = value

    def __str__(self):
        return repr(self.value)
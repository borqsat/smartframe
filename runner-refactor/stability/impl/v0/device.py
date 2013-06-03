#!/usr/bin/env python  
#coding: utf-8

class DeviceManager(object):
    '''DeviceManager maintains collecion of availiable devices'''

    def __init__(self):
        '''Init DeviceManager Instance.'''
        self._devices = list()

    @staticmethod
    def getInstance(context=None):
        pass

    def setContext(self, context=None):
        pass
        
    #@device
    def getDevice(self):
        pass

    def getDevices(self):
        pass

class BaseDevice(object):
    '''
    Abstract class for respresenting device instance ability.
    The instance of BaseDevice should provide the connection and basic actions for Device.
    '''

    def __init__(self):
        '''
        Abstract class for device.
        '''
        pass

    def __call__(self):
        return self

    def getSerialId(self):
        '''Return the device serial number from environment export '''
        pass
        
    def getConnect(self):
        '''
        connected to the device and get an impl for our access to real device.
        '''
        pass

    def resumeConnect(self):
        '''
        re-connected the device and get an impl for our access to real device.
        '''
        pass

    def getDeviceProperties(self):
        '''Return the device property value.'''
        pass

    def sleep(self,tsec):
        '''Test Action'''
        pass

    def launch(self,app_name):
        '''Test Action'''
        pass

    def press(self, key_name):
        '''Test Action'''
        pass

    def drag(self,start,end,time,steps):
        '''Test Action'''
        pass

    def swipe(self,start,end,time,steps):
        '''Test Action'''
        pass

    def touch(self,x,y):
        '''Test Action'''
        pass

    def input(self,content):
        '''Test Action'''
        pass

    def takeSnapshot(self,save_path):
        '''Test Action'''
        pass

    def internalCommand(self, command):
        '''Test Action'''
        pass

class Android_Device(BaseDevice):
    pass

class Tizen_Device(BaseDevice):
    pass
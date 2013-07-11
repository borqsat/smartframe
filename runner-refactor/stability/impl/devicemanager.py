#!/usr/bin/env python  
#coding: utf-8
'''
Module provides the function to maintain collecion of availiable devices. and the class represent a device instance.
@version: 1.0
@author: borqsat
@see: null
'''
__all__ = ['DeviceManager','DeviceRecoverException','DeviceInitException']

import time,sys,os,threading
from ability import Ability
import ConfigParser
import variables

class BACKDeviceManager(object):
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
            self._devices.append(self._device)
            return self._device
        except DeviceInitException,e1:
            print e1
            return None
        except DeviceRecoverException,e2:
            print e2
            return None

    def getDevices(self):
        '''
        Get the device collection list.
        '''
        return self._devices

class DevManager(object):
    '''DeviceManager maintains collecion of availiable devices'''

    def __init__(self,config=None):
        '''Init DeviceManager Instance.'''
        self._devices = list()
        self._device = None
        try:
            cf = ConfigParser.ConfigParser()
            cf.read(config)
            self._platform = cf.get('device','platform')
            #print self._platform
        except Exception, e:
            print 'invalid config file %s\n' % config

    def getDevice(self):
        '''
        Get instance of target device.
        rtype : the subclass of BaseDevice
        rparam : the subclass instance  of BaseDevice
        Exception: Throw exception when device init failed or recover failed.
        '''
        try:
            module = __import__('stability.impl.%s' % self._platform, fromlist=['Device'])
        except Exception,e :
            print e
            print '__import__ %s%s failed' % ('stability.impl.', self._platform)
        device = getattr(module, 'Device')
        try:
            if not self._device:
                self._device = device()
            if not self._device.available():
                self._device.recover()
            self._devices.append(self._device)
            return self._device
        except DeviceInitException,e1:
            print e1
            return None
        except DeviceRecoverException,e2:
            print e2
            return None

    def getDevices(self):
        '''
        Get the device collection list.
        '''
        return self._devices

DeviceManager = DevManager(config=variables.DEVICE_CONFIG_PATH)

class BaseDevice(Ability):
    '''
    Abstract class for respresenting device instance ability.
    The subclass of BaseDevice should extends from this class. and implement available() 
    recover() destory() method. and provide the ability to interacte with device. E.g: touch , press.
    takeSnapshot()
    '''
    #TODO set the subclass method behavor
    #def __init__(self):
    #    print set(dir(self.__class__)) - set(dir(BaseDevice))
    #    pass

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

    def destory(self):
        '''
        Release resource related to device instance.The method will be invoked before try
        to create a new device instance.
        '''
        pass

    def touch(self,*argv,**kwags):
        '''
        Simulates a touch event to the screen.
        The subclass MUST provide touch(x,y) operation.E.g touch(x,y)
        @type x: integer
        @param x: The horizontal position of the touch in actual device pixels, 
        starting from the left of the screen in its current orientation.
        @type y: integer
        @param y: The vertical position of the touch in actual device pixels, starting from the top of the screen in its current orientation. 
        '''
        pass

    def input(self,text):
        '''
        Sends the characters contained in text to device. Used to input text in the device
        editable region.
        @type text: string
        @param text: A string containing the characters to send.    
        '''
        pass

    def swipe(self,start,end):
        '''
        Simulates a swipe gesture (touch and move) on device's screen.
        @type start:  tuple 
        @param start: The starting point of the swipe gesture, in the form of a tuple (x,y) where x and y are integers.
        @type end:  tuple
        @param end: The end point of the swipe gesture, in the form of a tuple (x,y) where x and y are integers.
        '''
        pass

    def press(self,key_name):
        '''
        Sends the key event specified by type to the key specified by keycode.
        e.g: press('home')
        @type key_name: string
        @param key_name: The name of the key to send. MUST support 'home','back'
        '''
        pass

    def getDeviceProperties(self):
        '''
        Get device system properties dictionary.
        rtype {}
        rparam return the dictionary contains the device properties name and value. 
               e.g: {'uptime'  : The number of milliseconds since the device rebooted,
                     'product' : The overall product name,
                     'revision': build number of device}
        '''
        pass
        

    def getDeviceInfo(self,dest_folder):
        '''
        Pull device memory usage file to dest_folder.
        @type dest_folder: string
        @param dest_folder: The folder path used to store device log.
        '''        
        pass

    def takeSnapshot(self, save_path):
        '''
        Captures the entire screen of the current display and Writes the current image 
        to save_path in the format PNG.
        @type save_path: string
        @param save_path: The fully-qualified filename and extension of the output file.
        '''
        pass

    def catchLog(self, dest_folder):
        '''
        Pull device log file to dest_folder.
        @type dest_folder: string
        @param dest_folder: The folder path used to store device log.
        '''
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
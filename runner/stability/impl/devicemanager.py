#!/usr/bin/env python
import time,sys,os
import threading
from device import AndroidDevice
from stability.util.log import Logger

class DeviceManager(object):
    '''DeviceManager maintains collecion of availiable devices'''
    _instance = None
    _mutex = threading.Lock()

    def __init__(self):
        self._devices = list()
        self.logger = Logger.getLogger()
        self.logger.debug('init DeviceManager instance!')

    @staticmethod
    def getInstance(context=None):
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
        self._context = context

    def getDevice(self):
        #todo
        #provides more device type, only android target currently
        self.logger.debug('get device instance!')
        self._device = AndroidDevice()
        self._device.getConnect()
        self._devices.append(self._device)
        return self._device

    def getDeviceState(self,serial=None):
        return self._device.getState()

    def getDevices(self):
        return self._devices

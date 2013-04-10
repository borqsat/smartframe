'''
Module provides the function to maintain collecion of availiable devices.
@version: 1.0
@author: borqsat
@see: null
'''

import time,sys,os,threading
if str(sys.path).find('monkeyrunner.jar') != -1:
    from device import AndroidDevice as device
elif str(sys.path).find('tizenrunner.jar') != -1:
    from device import TizenDevice as device
from stability.util.log import Logger

class DeviceManager(object):
    '''DeviceManager maintains collecion of availiable devices'''
    _instance = None
    _mutex = threading.Lock()

    def __init__(self):
        '''Init DeviceManager Instance.'''
        self._devices = list()
        self.logger = Logger.getLogger()
        self.logger.debug('DEV: init DeviceManager instance!')

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
        '''set session context if exists'''
        self._context = context

    def getDevice(self):
        '''Get instance of device '''
        self.logger.debug('DEV: get device instance.')
        self._device = device()
        self._device.getConnect()
        self._devices.append(self._device)
        return self._device

    def getDeviceState(self,serial=None):
        '''Get the connected device status '''
        return self._device.getState()

    def getDevices(self):
        '''Get the device collection list'''
        return self._devices

'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import time,sys,os,threading
if str(sys.path).find('monkeyrunner.jar') != -1:
    from device import AndroidDevice as device
elif str(sys.path).find('tizenrunner.jar') != -1:
    from device import TizenDevice as device
from stability.util.log import Logger

class DeviceManager(object):
    '''DeviceManager maintains the collecion of availiable devices'''
    _instance = None
    _mutex = threading.Lock()

    def __init__(self):
        '''Init DeviceManager instance'''
        self._devices = list()
        self.logger = Logger.getLogger()
        self.logger.debug('DEV: init DeviceManager instance!')

    @staticmethod
    def getInstance(context=None):
        '''Get the instance of DeviceManager'''
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
        '''Set the application context'''
        self._context = context

    def getDevice(self):
        '''Get an available device instance'''
        self.logger.debug('DEV: get device instance.')
        self._device = device()
        self._device.getConnect()
        self._devices.append(self._device)
        return self._device

    def getDeviceState(self,serial=None):
        '''Get the device status'''
        return self._device.getState()

    def getDevices(self):
        '''Get the devices list holds by DeviceManager'''
        return self._devices

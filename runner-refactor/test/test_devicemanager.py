#!/usr/bin/env python  
#coding: utf-8

from stability.impl.devicemanager import DeviceManager,BaseDevice
import unittest


class TestDeviceManager(unittest.TestCase):
    def setUp(self):
        self._origin_getDevice = getattr(DeviceManager, 'getDevice')
        setattr(DeviceManager,'getDevice',self.getDevice)
        self._platform = 'test'
        self._dm = DeviceManager.getInstance(self._platform)
    	
    def tearDown(self):
        setattr(DeviceManager,'getDevice',self._origin_getDevice)

    def getDevice(self):
        return BaseDevice()

    def testSetContext(self):
        assert self._platform == getattr(self._dm, 'platform', None)

	def testGetInstance(self):
		assert self._dm is DeviceManager.getInstance()
		
    def testGetDevice(self):
    	device = self._dm.getDevice()
    	assert device is not None
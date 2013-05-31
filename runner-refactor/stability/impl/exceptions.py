#!/usr/bin/env python  
#coding: utf-8

'''
Module define exceptions in smart runner.
@version: 1.0
@author: borqsat
@see: null
'''

class FileNotFoundException(Exception):
    '''config file exception'''
    pass

class DebugBridgeException(Exception):
	'''adb or sdb exception'''
	pass

class DevicePowerDownException(Exception):
    '''
    Device offline exceptions.
    '''
	pass

class DeviceRebootException(Exception):
    '''
    Device offline exceptions.
    '''
	pass
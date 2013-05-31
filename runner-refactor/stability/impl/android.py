#!/usr/bin/env python  
#coding: utf-8

'''
Android device implemention.
@version: 1.0
@author: borqsat
@see: null
'''

from device import BaseDevice
from commands import getoutput as call

class Device(BaseDevice):
    def __init__(self):
        '''Andorid Device for Android platform'''
        super(Device,self).__init__()
        self.impl = None

    def getSerialId(self):
        '''Return the device serial number from environment export '''
        pass

    def getConnect(self):
        '''Connected to real Android Device'''
        self.impl = None

    def resumeConnect(self):
        '''Re-connected to real Android Device'''
        self.impl = None

    def touch(self,x):
        call('adb shell sh /data/local/tmp/phone.sh')

    def press(self,key):
        print ''

    def takeSnapshot(self,path):
        call('adb shell screencap /sdcard/sc.png')
        call('adb pull /sdcard/sc.png ' + path)



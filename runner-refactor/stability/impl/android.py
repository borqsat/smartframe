#!/usr/bin/env python  
#coding: utf-8

'''
Android device implemention.
@version: 1.0
@author: borqsat
@see: null
'''

from devicemanager import BaseDevice,DeviceInitException,DeviceRecoverException
from commands import getoutput as call
from log import logger
import socket

class Device(BaseDevice):
    def __init__(self):
        '''Andorid Device for Android platform'''
        super(Device,self).__init__()
        try:
            self._con = self.__getConnect()
        except:
            raise DeviceInitException('device instance init failed!')

    #def __get__(self, obj, type=None):
    #    print '-----get-----'
    #    print obj
    #    print self.__class__()
    #    print self
    #    return obj and self.__class__() or self   

    def __getConnect(self):
        #call('adb shell monkey --port 12345')
        call('adb forward tcp:12345 tcp:12345')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 12345))
        return s

    def available(self):
        print 'avaiable:%s'% self._con and True or False
        return self._con and True or False

    def recover(self):
        print 'recover'
        call('adb kill-server')
        call('adb start-server')
        #call('adb shell monkey --port 12345 > /dev/null')
        #call('adb forward tcp:12345 tcp:12345')
        try:
            self._con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._con.connect(('127.0.0.1', 12345))
        except:
            raise DeviceRecoverException('device recover failed!')

    def touch(self,x,y):
        cmd = '%s %s %s\n'%('tap',x,y)
        self._con.send(cmd)
        print self._con.recv(1024)
        return self

    def takeSnapshot(self,path):
        call('adb shell screencap /sdcard/sc.png')
        call('adb pull /sdcard/sc.png %s' % path)

    def catchLog(self,dest):
        call('adb pull /data/logs/aplog %s' % dest)

    def destory(self):
        print 'destory'
        if self._con:
            self._con.close()
#!/usr/bin/env python  
#coding: utf-8

'''
Android device implemention.
@version: 1.0
@author: maying
@see: null
'''

from devicemanager import BaseDevice,DeviceInitException,DeviceRecoverException
from commands import getoutput as call
from log import logger
import socket
import json
import subprocess
import time,string

PATH = '/data/logs; /data/anr'
IP = '127.0.0.1'
PORT = 5000
class Device(BaseDevice):
    def __init__(self):
        '''Andorid Device for Android platform'''
        super(Device,self).__init__()
        self.__getConnect()
    
    def __getConnect(self):
        '''
        Get connect from the socket in device
        '''
        process_id = call("adb shell ps|grep uiautomator|awk '{print $2}'")
        if process_id is not None and process_id != "":
            call("adb shell kill -9 %s"%process_id)
        call("adb forward tcp:%i tcp:%i"% (PORT, PORT))
        subprocess.Popen("adb shell uiautomator runtest /mnt/sdcard/EasyAutomator.jar -c com.borqs.easyautomator.EasyAutomator", shell=True)
        time.sleep(2)

    def available(self):
        '''
        Send request to the socket and check if can get response, 
        if yes, return True, else, return False.
        '''
        con = None
        try:
            jsonstring = {"action":"connect"}
            data = json.dumps(jsonstring)
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect((IP, PORT))
            con.send(data)
            result = con.recv(1024)
        except:
            result = "false"
        finally:
            if con != None:
                con.close()
        if result == "true":
            return True
        return False

    def recover(self):
        '''
        1.Check adb status
        2.Socket handle itself
        '''
        pass

    def touch(self, x, y):
        '''
        Perform a touch screen event
        Steps:
              1.Send request to touch screen.
              2.Get response from device and print log to logfile.
        Return:
              self
        Request protocol:{"action":"touch", "type":"point", "para":{"x":<x>, "y":<y>}}
                         para: Detail data for type.
                         eg: {"action":"touch", "type":"point", "para":{"x":0, "y":0}}
        Response data: {"result":<result>}
                       result: true, false
        '''
        con = None
        try:
            jsonstring = {"action":"touch", "type":"point", "para":{"x":x, "y":y}}
            data = json.dumps(jsonstring)
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect((IP, PORT))
            con.send(data)
            result = con.recv(1024)
            logger.debug("Press screen ("+x+", "+y+") result is " + result)
        except:
            logger.debug("Press screen ("+x+", "+y+") result return error")            
        finally:
            if con != None:
                con.close()
        return self

    def input(self, text):
        '''
        Input words to the focused EditText on the scree.
        Steps:
              1.Send request to input words.
              2.Get response from device and print log to log file.
        Return:
              self
        Request protocol:{"action":"input", "para":{"text": <text>}}
                         eg: {"action":"input", "para"{"text":"text"}}
        Response data: {"result":<result>}
                       result: true, false
        '''
        con = None
        try:
            jsonstring = {"action":"input", "para":{"text": text}}
            data = json.dumps(jsonstring)   
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect((IP, PORT))
            con.send(data)
            result = con.recv(1024)
            logger.debug("Input text:"+text+" result is " + result)
        except:
            logger.debug("Input text:"+text+" result return error")
        finally:
            if con != None:
                con.close()            
        return self

    def swipe(self, start, end):
        '''
        Perform a long click screen event
        Steps:
              1.Send request to drag device screen from start to end.
              2.Get response from device and print log to log file.
        Return:
              self
        Request protocol:{"action":"swipe", "para":{"x0": <x0>, "y0": <y0>, "x1": <x1>, "y1": <y1>, "steps":<steps>}}
                         
                         eg: {"action":"swipe", "para":{"x0": 15, "y0": 15, "x1": 15, "y1": 15, "steps":2,"steps": "2"}}
        Response data: {"result":<result>}
                       result: true, false
        '''
        con = None
        try:
            jsonstring = {"action":"swipe", "para":{"x0": x0, "y0": y0, "x1": x1, "y1": y1, "steps": 100}}
            data = json.dumps(jsonstring)
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect((IP, PORT))
            con.send(data)
            result = con.recv(1024)
            logger.debug("Swipe from ("+x0+", "+y0+") to ("+x1+", "+y1+") result is " + result)        
        except:
            logger.debug("Swipe from ("+x0+", "+y0+") to ("+x1+", "+y1+") result return error")            
        finally:
            if con != None:
                con.close()       
        return self

    def press(self,key_name):
        '''
        Perform a key event.
        Steps:
              1.Send request to press keyevent.
              2.Get response from device and print log to log file.
        Return:
              self
        Request protocol:{"action":"press", "para":{"key":<key_name>}} 
                         key_name:up, down, left, center, delete, search, menu, Recent_apps, back 
        Response data: {"result":<result>}
                       result: true, false
        '''
        con = None
        try:
            jsonstring = {"action":"press", "para":{"key":key_name}}
            data = json.dumps(jsonstring)
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect((IP, PORT))
            con.send(data)
            result = con.recv(1024)
            logger.debug("Send keyevent: "+key_name+" result is " + result)
        except:
            logger.debug("Send keyevent: "+key_name+" result return error")       
        finally:
            if con != None:
                con.close()   
        return self


    def getDeviceProperties(self):
        '''
        Get device properties
        Steps:
              1.adb shell getprop ***.
        Return:
              dictionary 
               e.g: {'uptime'  : The number of milliseconds since the device rebooted,
                     'product' : The overall product name,
                     'revision': build number of device}
        '''
        product = commands.getoutput("adb shell getprop ro.product.name")
        uptime = commands.getoutput("adb shell getprop ro.runtime.firstboot")
        revision = commands.getoutput("adb shell getprop ro.build.revision")
        return dic
        

    def getDeviceInfo(self,dest_folder):
        '''
        Pull device memory usage file to dest_folder.
        @type dest_folder: string
        @param dest_folder: The folder path used to store device log.
        '''        
        pass

    def takeSnapshot(self, save_path):
        '''
        Take a screenshot and save to path.
        Steps:
              1.Send request to take snapshot.
              2.Check if the snapshot is exist, if no, print log to log file.
              3.If yes, pull snapshot to the path on PC
        Return:
              self
        Request protocol:{"action":"screensnap", "para":{"scale": 1.0, "quality": 0.9}}
        Response data: {"result":<result>}
                       result: true, false
        '''
        build_version = commands.getoutput("adb shell getprop ro.build.version.release")
        version_list = string.split(build_version, '.')
        if string.atoi(version_list[0]) > 3 and string.atoi(version_list[1]) > 1:
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect((IP, PORT))
            jsonstring = {"action":"screensnap", "para":{"scale": 1.0, "quality": 0.9}}
            data = json.dumps(jsonstring)
            con.send(data)
            logger.debug("Take screen snapshot result is " + con.recv(1024))
            result = commands.getoutput("adb pull /mnt/sdcard/picture/a.png %s"%save_path)
            if result.contains("fail"):
                logger.debug("Pull picture fail!")
        else:
            call('adb shell mkdir /mnt/sdcard/picture')
            call('adb shell screenshot /mnt/sdcard/picture/a.png')
            result = commands.getoutput("adb pull /mnt/sdcard/picture/a.png %s"%save_path)
            if result.contains("fail"):
                logger.debug("Pull picture fail!")
        return self

    def catchLog(self, dest_folder):
        '''
        Pull device log file to dest_folder.
        @type dest_folder: string
        @param dest_folder: The folder path used to store device log.
        '''
        log_list = string.split(PATH,';')
        for item in log_list:
            commands.getoutput("sdb pull %s %s"%(item, dest_folder))

    
    def touch(self, touch_type, type_value):
        '''
        Perform a touch screen event
        Steps:
              1.Send request to touch screen.
              2.Get response from device and print log to logfile.
        Return:
              self
        Request protocol:{"action":"click", "type":<type>, "para":{"type_value":<value>}}
                         type: text | d | dc| dm | ds...
                         para: Detail data for type.
                         eg: {"action":"click", "type":"text", "para":{"type_value":"text_value"}}
        Response data: {"result":<result>}
                       result: true, false
        '''
        return self

    def touchAndWaitforWindow(self, touch_type, value, time=1000):
        '''
        Perform a touch screen event and wait for new window opened.
        Steps:
              1.Send request to touch screen.
              2.Get response from device and print log to logfile.
        Return:
              self
        Request protocol:{"action":"clickAndWaitForNewWindow", "para":{"type":<type>, "type_value":<value>, "time":<time>}}
                         type: text | d | dc| dm | ds...
                         para: Detail data for type.
                         eg: {"action":"click", "para":{"type":"text", "type_value":"application", "time":"10"}}
        Response data: {"result":<result>}
                       result: true, false
        '''
        return self


    def long_touch(self, touch_type, para):
        '''
        Perform a long click screen event
        Steps:
              1.Send request to long click a view on screen.
              2.Get response from device and print log to log file.
        Return:
              self
        Request protocol:{"action":"long_click", "para":{"type":<type>, "type_value":<value>}}
                         type: text | d | dc| dm | ds...
                         para: Detail data for type.
                         eg: {"action":"click", "para":{"type":"text", "type_value":"application"}}
        Response data: {"result":<result>}
                       result: true, false
        '''
        return self

    def clear_input(self):
       '''
       Clear words for the focused EditText on the scree.
        Steps:
              1.Send request to clear words.
              2.Get response from device and print log to log file.
        Return:
              self
        Request protocol:{"action":"clearTextField"}
        Response data: {"result":<result>}
                       result: true, false
       '''
       return self
     

    def takeSnapshot(self, path, scale=1.0, quality=0.9):
        '''
        Take a screenshot and save to path.
        Steps:
              1.Send request to take snapshot.
              2.Check if the snapshot is exist, if no, print log to log file.
              3.If yes, pull snapshot to the path on PC
        Return:
              self
        Request protocol:{"action":"screensnap", "para":{"scale": <scale>, "quality": <quality>}}
        Response data: {"result":<result>}
                       result: true, false
        '''
        return self
 

    def getCurrentActivityName(self):
        '''
        Get current activity name.
        Steps:
              1.Send request to get current activity name
        Return:
              dictionary 
        Request protocol:{"action":"getCurrentActivityName"}
        Response data: {"result":<activity_name>}
        '''

        return ""

    def getText(self, view_type, value):
        '''
        Get text of a view on the screen
        Steps:
              1.Send request to get text of a view on the screen
        Return:
              dictionary 
        Request protocol:{"action":"getText", "para":{"type":<type>, "type_value":<value>}}
                         type: d | dc| dm | ds | selected ...
                         para: Detail data for type.
        Response data: {"result":<text>}
        '''
        return ""

    def setOrientation(self, position):
        '''
        Set orientation to a direction.
        Steps:
              1.Send request to set orientation.
              2.Get response from device and print log to log file.
        Return:
              self
        Request protocol:{"action":"setOrientation", "para":{"direction":<direction>}}
                         direction:left, right, natural
        Response data: {"result":<result>}
                       result: true, false
        '''
        return self
        


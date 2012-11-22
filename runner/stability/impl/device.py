'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import time, sys, os, shutil, datetime, string, uuid
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from stability.util.log import Logger

# Env name of device serial for adb connection.
_ANDROID_SERIAL = 'ANDROID_SERIAL'
def _getSerial():
    global _ANDROID_SERIAL
    if (os.environ.has_key(_ANDROID_SERIAL)):
        return os.environ[_ANDROID_SERIAL]
    else:
        return None

# get MonkeyDevice
_device = None
def _getMonkeyDevice(serial=None):
    # Wait for the device
    global _device
    reconnect = False
    if _device is None:
        logger = Logger.getLogger()
        logger.debug('Device is None. Got device again...')
        reconnect = True
    else:
        try:
            _device.wake()
        except:
            reconnect = True
    if reconnect:
        if (serial is None or '' == serial):
            _device = MonkeyRunner.waitForConnection(timeout=15)
        else:
            _device = MonkeyRunner.waitForConnection(timeout=15, deviceId=serial)
    return _device

def reconnect(msg=None):
    global _device
    _device = None

# Device STATE CODES
DEVICE_DISCONNECTED = 0x00000000
DEVICE_IDLE = 0x00000001
DEVICE_CONNECTED = 0x00000002
DEVICE_ERROR = 0x00000003
DEVICE_USED = 0x00000004

class AndroidDevice:
    '''AndroidDevice provides the connection and basic actions for Android Device'''

    def __init__(self, serial=None):
        '''context is context of current running test session.'''
        #if not defined, use the system envrionment value
        if serial is None:
            self.serial = _getSerial()
        else:
            self.serial = serial
        self.logger = Logger.getLogger()
        self._state = DEVICE_DISCONNECTED
        self.logger.debug('init device instance!')

    def getConnect(self):
        '''use the monkeydevice impl for our access to android device'''
        self.impl = _getMonkeyDevice(self.serial)
        if not self.impl is None:
            self.properties = self.getDeviceProperties()
            self._state = DEVICE_CONNECTED
        else:
            self.properties = None
            self._state = DEVICE_ERROR
        return self

    def resumeConnect(self):
        self.logger.debug('******************************resume connect*********************************')
        self.impl = _getMonkeyDevice(self.serial)
        self._state = DEVICE_CONNECTED
        return self

    def getDeviceId(self):
        return str(uuid.uuid1())

    def getDeviceInfo(self):
        result = {}
        if not self.impl is None:
            #result['product'] = 'AT390'
            #result['revision'] = '6628'
            result['product'] = self.impl.getSystemProperty('ro.build.product')
            result['revision'] = self.impl.getSystemProperty('ro.build.revision')
            result['width'] = self.impl.getProperty('display.width')
            result['height'] = self.impl.getProperty('display.height')
        return result

    def getDeviceProperties(self):
        properties = {}
        try:
            properties['display.width'] = self.impl.getProperty('display.width')
            self.logger.debug(properties['display.width'])
            properties['display.height'] = self.impl.getProperty('display.height')
            self.logger.debug(properties['display.height'])
            properties['display.density'] = self.impl.getProperty('display.density')
            for k in properties.keys():
                self.logger.debug(k + ' = ' + properties[k])
        except Exception, e:
            self.logger.debug('Exception during retrieving properties!')
            self.logger.debug('Adb connection error!')
            global _device
            _device = None
        return properties

    def convert_to_screen_rect(self, rect):
        left = rect[0]
        top = rect[1]
        right = rect[2]
        bottom = rect[3]
        left = int(left*int(self.properties['display.width']))
        right = int(right*int(self.properties['display.width']))
        top = int(top*int(self.properties['display.height']))
        bottom = int(bottom*int(self.properties['display.height']))
        # check if name is valid
        # check if the rectangle is in the screen
        #self.assertTrue(0<=left and left < right and right <= self.display_width)
        #self.assertTrue(0<=top and top < bottom and bottom <= self.display_height)
        return (left, top, right-left, bottom-top)

    def getState(self):
        return self._state

    def _pressSeq(self, keySeq,interval=None):
    #@param keySeq: eg:'up,up,down'
        seq = string.lower(keySeq)
        len(seq)
        eventList = string.split(seq, ',')
        for event in eventList:
            event = event.strip()
            self._press(event)
            if interval:
                MonkeyRunner.sleep(interval)

    def _press(self, keyEvent):
    #@parm keyEvent: single key event
        if keyEvent == 'up':
            key = 'KEYCODE_DPAD_UP'
            self.logger.debug('KEYCODE_DPAD_UP')
        elif keyEvent == 'down':
            key = 'KEYCODE_DPAD_DOWN'
            self.logger.debug('KEYCODE_DPAD_DOWN')
        elif keyEvent == 'right':
            key = 'KEYCODE_DPAD_RIGHT'
            self.logger.debug('KEYCODE_DPAD_RIGHT')
        elif keyEvent == 'left':
            key = 'KEYCODE_DPAD_LEFT'
            self.logger.debug('KEYCODE_DPAD_LEFT')
        elif keyEvent == 'menu':
            key = 'KEYCODE_MENU'
            self.logger.debug('KEYCODE_DPAD_MENU')
        elif keyEvent == 'center':
            key = 'KEYCODE_DPAD_CENTER'
            self.logger.debug('KEYCODE_DPAD_CENTER')
        elif keyEvent == 'back':
            key = 'KEYCODE_BACK'
            self.logger.debug('KEYCODE_DPAD_BACK')
        try:
            self.impl.press(key, 'DOWN_AND_UP')
        except:
            self.logger.debug('Error during press key!!!')

    def sleep(self,tsec):
        MonkeyRunner.sleep(tsec)
        return self

    def startActivity(self, component, flags,data,action,uri,mimetype,categories,extras):
        try:
            self.impl.startActivity(component=component, flags=flags,data=data,action=action,uri=uri,mimetype=mimetype,categories=categories,extras=extras)
        except:
            self.logger.debug('Error during startActivity with component name: {%s} !!!' % 'fail')

    def pressKey(self, keyseq,interval=None):
        try:
            self.logger.debug('Press key: %s'%(keyseq) )
            self._pressSeq(keyseq,interval=interval)
        except:
            self.logger.debug('Error during pressKey!!!')

    def drag(self,start,end,time,steps):
        try:
            self.logger.debug('Drag.')
            self.impl.drag(start,end,time,steps)
        except:
            self.logger.debug('Error during DragDrop!!!')

    def touch(self,x,y):
        try:
            self.logger.debug('Touch.')
            self.impl.touch(x,y,'DOWN_AND_UP')
        except:
            self.logger.debug('Error during touch!!!') 

    def typeWord(self,content):
        try:
            self.logger.debug('type word.')
            self.impl.type(content)
            #MonkeyRunner.sleep(3)
        except:
            self.logger.debug('Error during typeWord!!!')

    def takeSnapshot(self):
        try:
            # Takes a screenshot
            self.logger.debug('Screen SnapShot.' )
            result = self.impl.takeSnapshot()
        except:
            result = None
            self.logger.debug('Error during SnapShot!!!')
        return result

    def screenSnapShot(self, filePath, ext):
        try:
            # Takes a screenshot
            self.logger.debug('Screen SnapShot.' )
            result = self.impl.takeSnapshot()
            # Writes the screenshot to a file
            result.writeToFile(filePath, ext)
        except:
            self.logger.debug('Error during SnapShot!!!')

    def adbcommand(self, command):
        try:
            # Takes a screenshot
            self.logger.debug('ADB Shell command.' )
            result = self.impl.shell(command)
            return result
        except:
            self.logger.debug('Error during adb command!!!')

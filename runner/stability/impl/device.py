'''
Module provides the function to interact with device.
@version: 1.0
@author: borqsat
@see: null
'''
import time, sys, os, shutil, datetime, string, uuid, commands, socket
from stability.util.log import Logger
from exceptions import DeviceException
if str(sys.path).find('monkeyrunner.jar') != -1:
    from com.android.monkeyrunner import MonkeyRunner as runner
    from com.android.monkeyrunner import MonkeyDevice as device
    DEVICE = 'android'
    _DEVICE_SERIAL = 'ANDROID_SERIAL'
    DEVICE_UPTIME = 'clock.realtime'
    DEVICE_ERROR_TAG = ['device not found','offline']
    DEVICE_SHELL_TAG = 'adb shell ps'
    DEVICE_DAEMON_TAG = 'com.android.commands.monkey'
    EXCEPTION_DAEMON = 'monkey exit'
    EXCEPTION_BRIDGE = 'ADB connection exception'
elif str(sys.path).find('tizenrunner.jar') != -1:
    from com.tizen.tizenrunner import TizenRunner as runner
    from com.tizen.tizenrunner import TizenDevice as device
    DEVICE = 'tizen'
    _DEVICE_SERIAL = 'TIZEN_SERIAL'
    DEVICE_UPTIME = ''
    DEVICE_ERROR_TAG = ['device not found','offline','error']
    DEVICE_SHELL_TAG = 'sdb shell ps -aux | grep GASClient'
    DEVICE_DAEMON_TAG = 'GASClient'
    EXCEPTION_DAEMON = 'GASClient exit'
    EXCEPTION_BRIDGE = 'SDB connection exception'

_device = None
def _getSerial():
    '''get device serial number which specify by export XXXX_SERIAL=xxxx '''
    global _DEVICE_SERIAL
    if (os.environ.has_key(_DEVICE_SERIAL)):
        return os.environ[_DEVICE_SERIAL]
    else:
        return None

def getAvailablePort():
    '''find an available local port to forward'''
    host = '127.0.0.1'
    available_port = 9000
    time_out = 2
    while True:
        sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sk.settimeout(time_out)
        try:
            sk.bind((host,available_port))
            sk.close()
            bflag = False
        except socket.error, e:
            if e.errno == 98 or e.errno == 13:
                bflag = True
        if bflag: available_port += 1
        else: break
    return available_port

def _getDevice(serial=None):
    '''get target device instance '''
    logger = Logger.getLogger()
    # Wait for the device
    global _device
    reconnect = False
    if _device is None:
        logger.debug('DEV: device instance is None. try to device...')
        reconnect = True
    else:
        try:
            _device.wake()
            checkDeviceStatus(DEVICE,_device)
        except:
            logger.debug('DEV: device unavailable. try to get device again...')
            reconnect = True
    if reconnect:
        _device = None
        local_port = getAvailablePort()
        logger.debug('%s %s' % ('DEV: got available port ', str(local_port)))
        try:
            if (serial is None or '' == serial):
                if DEVICE == 'tizen':
                    _device = runner.waitForConnection(localport=local_port,remoteport=3490)
                elif DEVICE == 'android':
                    _device = runner.waitForConnection()
                logger.debug('DEV: got device with serial number unspecified.')
            else:
                if DEVICE == 'tizen':
                    _device = runner.waitForConnection(deviceId=serial,localport=local_port,remoteport=3490)
                elif DEVICE == 'android':
                    _device = runner.waitForConnection(deviceId=serial)
                logger.debug('%s %s'% ('DEV: got device with serial number:',str(serial)))
        except Exception, e:
            logger.debug('%s %s' % ('Exception:',e))
            logger.debug('DEV: device may be already reboot or daemon exit.')
    return _device

def checkDeviceStatus(platform,device):
    '''Check the debug bridge status '''
    if platform == 'android':
        ret = device.getProperty(DEVICE_UPTIME)
        if ret is None:
            if serial:
                rets = commands.getoutput(DEVICE_SHELL_TAG)
            else:
                rets = commands.getoutput('%s %s %s' %('adb -s',serial,'shell ps'))
            if rets is not None:
                for i in DEVICE_ERROR_TAG:
                    if not rets.find(i) == -1:
                        raise DeviceException(i)
                if rets.find(DEVICE_DAEMON_TAG) == -1:
                    raise DeviceException(EXCEPTION_DAEMON)
                raise DeviceException(EXCEPTION_BRIDGE)

    if platform == 'tizen1':
        rets = commands.getoutput(DEVICE_SHELL_TAG)
        print 'tizen sdb shell ps -aux | grep GASClient::'
        print rets
        if rets is not None:
            for i in DEVICE_ERROR_TAG:
                if not rets.find(i) == -1:
                    raise DeviceException(i)
            if rets.find(DEVICE_DAEMON_TAG) == -1:
                raise DeviceException(EXCEPTION_DAEMON)
            #raise DeviceException(EXCEPTION_BRIDGE)

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
        self.logger.debug('DEV: init device instance.')

    def getConnect(self):
        '''use the monkeydevice impl for our access to android device'''
        self.impl = _getDevice(self.serial)
        if not self.impl is None:
            self.properties = self.getDeviceProperties()
            self._state = DEVICE_CONNECTED
        else:
            self.properties = None
            self._state = DEVICE_ERROR
        return self

    def resumeConnect(self):
        self.impl = _getDevice(self.serial)
        self._state = DEVICE_CONNECTED
        return self

    def getDeviceId(self):
        return self.serial

    def getDeviceInfo(self):
        result = {}
        if not self.impl is None:
            result['product'] = self.impl.getSystemProperty('ro.build.product')
            result['revision'] = self.impl.getSystemProperty('ro.build.revision')
            result['width'] = self.impl.getProperty('display.width')
            result['height'] = self.impl.getProperty('display.height')
        return result

    def getDeviceProperties(self):
        properties = {}
        try:
            properties['display.width'] = self.impl.getProperty('display.width')
            properties['display.height'] = self.impl.getProperty('display.height')
            properties['display.density'] = self.impl.getProperty('display.density')
            realtime = int(self.impl.getProperty('clock.realtime'))
            clock = int(self.impl.getProperty('clock.millis'))
            self.logger.debug('Phone uptime: %d hours %d minutes %d seconds, Phone Clock: %s' % (\
                              realtime/3600000,\
                              (realtime%3600000)/60000,\
                              (realtime%60000)/1000,\
                              time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime(clock/1000.))))
            for k in properties.keys():
                self.logger.debug(k + ' = ' + properties[k])
        except:
            pass 
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
        return (left, top, right-left, bottom-top)

    def getState(self):
        return self._state

    def _pressSeq(self, keySeq,interval=None):
    #@param keySeq: eg:'up,up,down'
        seq = string.lower(keySeq)
        eventList = string.split(seq, ',')
        for event in eventList:
            event = event.strip()
            self._press(event)
            if interval:
                runner.sleep(interval)

    def _press(self, keyEvent):
    #@parm keyEvent: single key event
        if keyEvent == 'up':
            key = 'KEYCODE_DPAD_UP'
        elif keyEvent == 'down':
            key = 'KEYCODE_DPAD_DOWN'
        elif keyEvent == 'right':
            key = 'KEYCODE_DPAD_RIGHT'
        elif keyEvent == 'left':
            key = 'KEYCODE_DPAD_LEFT'
        elif keyEvent == 'menu':
            key = 'KEYCODE_MENU'
        elif keyEvent == 'center':
            key = 'KEYCODE_DPAD_CENTER'
        elif keyEvent == 'back':
            key = 'KEYCODE_BACK'
        elif keyEvent == 'home':
            key = 'KEYCODE_HOME'
        else:
            key = string.upper(keyEvent)
        self.logger.debug('%s %s' % ('action press: ',key))

        try:
            self.impl.press(key, 'DOWN_AND_UP')
        except:
            self.logger.debug('action: Error during press key!!!')

    def sleep(self,tsec):
        runner.sleep(tsec)
        return self

    def startActivity(self, component, flags,data,action,uri,mimetype,categories,extras):
        try:
            self.impl.startActivity(component=component, flags=flags,data=data,action=action,uri=uri,mimetype=mimetype,categories=categories,extras=extras)
            self.logger.debug('%s %s' % ('action:  Launch activity = ',str(component)))
        except:
            self.logger.debug('Error during startActivity with component name: {%s} !!!' % 'fail')

    def pressKey(self, keyseq,interval=None):
        try:
            self.logger.debug('%s %s' % ('action: Press key ->',str(keyseq)))
            self._pressSeq(keyseq,interval=interval)
        except:
            self.logger.debug('Error during pressKey!!!')

    def drag(self,start,end,time,steps):
        try:
            self.logger.debug('action: Drag')
            self.impl.drag(start,end,time,steps)
        except:
            self.logger.debug('Error during DragDrop!!!')

    def touch(self,x,y):
        try:
            self.impl.touch(x,y,'DOWN_AND_UP')
        except:
            self.logger.debug('Error during touch!!!') 

    def typeWord(self,content):
        try:
            self.logger.debug('%s%s' % ('action: type word -> ',str(content)))
            self.impl.type(content)
        except:
            self.logger.debug('Error during typeWord!!!')

    def takeSnapshot(self,path):
        ret = False
        try:
            self.logger.debug('action: take snapshot')
            snapshot = self.impl.takeSnapshot()
            ret = snapshot.writeToFile(path)
        except:
            ret = False
            global _device
            _device = None
            #checkDeviceStatus(self.impl)
            self.logger.debug('Error during SnapShot!!!')
        finally:
            snapshot = None
            return ret

    def screenSnapShot(self, filePath, ext):
        try:
            # Takes a screenshot
            self.logger.debug('action: Screen SnapShot.' )
            result = self.impl.takeSnapshot()
            # Writes the screenshot to a file
            result.writeToFile(filePath, ext)
        except:
            self.logger.debug('Error during SnapShot!!!')

    def adbcommand(self, command):
        try:
            # Takes a screenshot
            self.logger.debug('%s%s' % ('action: Shell command-> ',str(command)))
            result = self.impl.shell(command)
            return result
        except:
            self.logger.debug('Error during adb command!!!')

class TizenDevice:
    '''TizenDevice provides the connection and basic actions for Tizen Device'''
    offset = None
    def __init__(self, serial=None):
        '''context is context of current running test session.'''
        #if not defined, use the system envrionment value
        if serial is None:
            self.serial = _getSerial()
        else:
            self.serial = serial
        self.offset = None
        self.logger = Logger.getLogger()
        self._state = DEVICE_DISCONNECTED
        self.logger.debug('DEV: init device instance.')

    def getConnect(self):
        '''use the tizendevice impl for our access to tizen device'''
        self.impl = _getDevice(self.serial)
        if not self.impl is None:
            self.properties = self.getDeviceProperties()
            self._state = DEVICE_CONNECTED
        else:
            self.properties = None
            self._state = DEVICE_ERROR
        return self

    def resumeConnect(self):
        self.impl = _getDevice(self.serial)
        self._state = DEVICE_CONNECTED
        return self

    def getDeviceId(self):
        return self.serial

    def getDeviceInfo(self):
        result = {}
        if not self.impl is None:
            result['product'] = 'tizen' #self.impl.getSystemProperty('ro.build.product')
            result['revision'] = 'unknown' #self.impl.getSystemProperty('ro.build.revision')
            result['width'] = '600'#self.impl.getProperty('display.width')
            result['height'] = '1024'#self.impl.getProperty('display.height')
        return result

    def getDeviceProperties(self):
        properties = {}
        try:
            properties['display.width'] = '600'#self.impl.getProperty('display.width')
            properties['display.height'] = '1024'#self.impl.getProperty('display.height')
            properties['display.density'] = 'unknown'#self.impl.getProperty('display.density')
            realtime = 1000#int(self.impl.getProperty('clock.realtime'))
            clock = 10000#int(self.impl.getProperty('clock.millis'))
            self.logger.debug('Phone uptime: %d hours %d minutes %d seconds, Phone Clock: %s' % (\
                              realtime/3600000,\
                              (realtime%3600000)/60000,\
                              (realtime%60000)/1000,\
                              time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime(clock/1000.))))
            for k in properties.keys():
                self.logger.debug(k + ' = ' + properties[k])
        except:
            pass 
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
        return (left, top, right-left, bottom-top)

    def getState(self):
        return self._state

    def _pressSeq(self, keySeq,interval=None):
    #@param keySeq: eg:'up,up,down'
        seq = string.lower(keySeq)
        eventList = string.split(seq, ',')
        for event in eventList:
            event = event.strip()
            self._press(event)
            if interval:
                runner.sleep(interval)

    def _press(self, keyEvent):
    #@parm keyEvent: single key event
        if keyEvent == 'shome':
            key = 'SHOME'
        elif keyEvent == 'lhome':
            key = 'LHOME'
        elif keyEvent == 'right':
            key = 'KEYCODE_DPAD_RIGHT'
        elif keyEvent == 'left':
            key = 'KEYCODE_DPAD_LEFT'
        elif keyEvent == 'menu':
            key = 'KEYCODE_MENU'
        elif keyEvent == 'center':
            key = 'KEYCODE_DPAD_CENTER'
        elif keyEvent == 'back':
            key = 'KEYCODE_BACK'
        elif keyEvent == 'home':
            key = 'KEYCODE_HOME'
        else:
            key = string.upper(keyEvent)
        self.logger.debug('%s %s' % ('action press: ',key))

        try:
            self.impl.press(key, 'DOWN_AND_UP')
        except:
            self.logger.debug('action: Error during press key!!!')

    def sleep(self,tsec):
        runner.sleep(tsec)
        return self

    def takeSnapshot(self,path):
        ret = False
        try:
            self.logger.debug('action: take snapshot')
            snapshot = self.impl.takeSnapshot()
            self.logger.debug('action: write snapshot to: ' + path)
            ret = snapshot.writeToFile(path)
            self.logger.debug('action: write snapshot end.')
        except:
            ret = False
            global _device
            _device = None
            checkDeviceStatus(DEVICE,self.impl)
            self.logger.debug('Error during SnapShot!!!')
        finally:
            return ret

    #here add offset to work round for tizen. 
    def touch(self,x,y):
        try:
            x = int(x*1024/600)
            if not TizenDevice.offset:
                TizenDevice.offset = (x,y)
            elif TizenDevice.offset == (x,y) :
                x = x + 1
                TizenDevice.offset = (x,y)
            else:
                TizenDevice.offset = (x,y)
            self.impl.touch(x,y,'DOWN_AND_UP')
        except:
            self.logger.debug('Error during device touch!!!')


    def pressKey(self, keyseq,interval=None):
        try:
            self.logger.debug('%s %s' % ('action: Press key ->',str(keyseq)))
            self._pressSeq(keyseq,interval=interval)
        except:
            self.logger.debug('Error during pressKey!!!')

    ###################################in current stage not support yet
    def startActivity(self, component, flags,data,action,uri,mimetype,categories,extras):
        try:
            assert False,"Device don't support this commmand"
            #self.logger.debug('%s %s' % ('action:  Launch activity = ',str(component)))
        except:
            self.logger.debug('Error during startActivity with component name: {%s} !!!' % 'fail')


    def drag(self,start,end,time,steps):
        try:
            self.logger.debug('action: Drag')
            assert False,"Device don't support this commmand"
        except:
            self.logger.debug('Error during DragDrop!!!')

    def typeWord(self,content):
        try:
            self.logger.debug('%s%s' % ('action: type word -> ',str(content)))
            assert False,"Device don't support this commmand"
        except:
            self.logger.debug('Error during typeWord!!!')

    #save current screen
    def screenSnapShot(self, filePath, ext):
        try:
            # Takes a screenshot
            self.logger.debug('action: Screen SnapShot.' )
            result = self.impl.takeSnapshot()
            # Writes the screenshot to a file
            result.writeToFile(filePath, ext)
        except:
            self.logger.debug('Error during SnapShot!!!')

    def adbcommand(self, command):
        try:
            # Takes a screenshot
            self.logger.debug('%s%s' % ('action: Shell command-> ',str(command)))
            assert False,"Device don't support this commmand"
        except:
            self.logger.debug('Error during adb command!!!')

#def invokeDeviceDaemon(timeout=None,serial=None):
#    import subprocess
#    subprocess.Popen(['sdb','forward','tcp:3490','tcp:3490'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
#    print 'forward ok'
#    subprocess.Popen(['sdb','shell','GASClient','/dev/input/event0','/dev/input/#event1'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
#    print 'GASClient start ok'
#    import time
#    time.sleep(3)

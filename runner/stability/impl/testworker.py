#!/usr/bin/env python  
#coding: utf-8  
''''' 
@author: Arthur 
@license: None 
@contact: hongbin.bao@borqs.com 
@see: www.borqs.com
 
@version: 1.0 
@todo[1.1]: a new story 
 
@note: SmartRunner  Doc
@attention: please attention 
@bug: None
@warning: None
'''  

import time,sys,os,shutil,datetime,string,unittest,ConfigParser
from devicemanager import DeviceManager
from expectresult import ExpectResult
from stability.util.log import Logger
from imglib import imglib
from pubsub import pub

class TestAction:
    '''
    Interface for sending test action.
    '''
    def setDeviceImpl(self,deviceImpl,config=None):
        '''
        Set the instance of device implement.
        @type deviceImpl: Object of device.
        @param deviceImpl: Instance of device.
        '''
        self.impl = deviceImpl
        self.config = config

    def launch(self,component=None,flags=0x04000000,data=None,action=None,uri=None,mimetype=None,categories=None,extras=None,waittime=None):
        '''
        Starts an Activity on this device by sending an Intent constructed from the supplied arguments.

        Arguments:
        @type component: String
        @param  component: The component for the Intent. Using this argument will direct the Intent to a specific class within a specific Android package.  
        @type flags: iterable
        @param flags: An iterable data structure containing flags that control how the Intent is handled.
        @type data: String
        @param data: The data URI for the Intent.
        @type action: String
        @param action: The action for the Intent.
        @type uri: String
        @param uri: The uri for the Intent.
        @type mimrtype: String
        @param mimetype: The MIME type for the Intent.
        @type categories: String
        @param categories: An iterable data structure containing strings that define categories for the Intent.
        @type extras: String
        @param extras: A dictionary of extra data for the Intent.
        @type waittime: Int
        @param waittime: The idle time after launching activity. The default value is 3 seconds. See "runner/stability/sysconfig"
        @rtype: device object
        @return: The instance of device object. 
        '''
        self.impl.startActivity(component, flags,data,action,uri,mimetype,categories,extras)
        if not waittime:
            waittime = int(self.config.get('time','after_launch_time'))
        self.impl.sleep(waittime)
        return self
    
    def press(self,keyseq,waittime=None):
        '''
        Sends the key event sequence specified by type to the key specified by keycode.

        @type keyseq: string
        @param keyseq: The key event sequence string split by character ','.
        @type waittime: int
        @param waittime: The idle time after press action. Default is 1 seconds after one key action. See "runner/stability/sysconfig"
        '''
        if not waittime:
            waittime = int(self.config.get('time','after_press_time'))
        self.impl.pressKey(keyseq,interval=waittime)
        return self

    def touch(self,arg,waittime=None):
        '''
        Sends a touch event to the device's scrren region or specified by type to the screen location specified 
        by x and y.

        @type arg: string or tuple 
        @param arg: 
        String : a image file path which contained in the current device's scrren 
        tuple: The screen location specified by x and y.
               Format: (x,y) the screen location specified by x and y.
               x   The horizontal position of the touch in actual device pixels, starting from the left of the screen in its current orientation.
               y   The vertical position of the touch in actual device pixels, starting from the top of the screen in its current orientation.
        @type waittime: int
        @param waittime: The idle time after touch action. Default value is 1 seconds. See "runner/stability/sysconfig"
        @rtype: device object
        @return: The instance of device object. 
        '''
        if not waittime:
            waittime = int(self.config.get('time','after_touch_time'))
        if isinstance(arg,str):
            path =  self.checker.testResult.dirs['all']
            #add 1120
            if arg.find('.png'):
                arg = arg.replace('.png','')

            smallSnapshot = self.checker.expectResult.getCurrentPath(arg)
            ###names = '%s.snapshot.png' % arg
            right_snapshot = self.checker.expectResult.getCurrentCheckPointParent()
            dirs,filename = os.path.split(right_snapshot)
            rect = filename.split('.')[1]
            names = '%s.%s.png' % (arg,rect)
            largeSnapshot = os.path.join(path, names)
            self.checker.capture(largeSnapshot,upload=True)
 
            point = imglib.getRegionCenterPoint(largeSnapshot,smallSnapshot)
            if not point:
                assert False,'Can find the matched image %s from %s ' % (smallSnapshot,largeSnapshot)
            self.impl.touch(int(point[0]),int(point[1]))
        elif isinstance(arg,tuple):
            self.impl.touch(arg[0],arg[1])
        self.impl.sleep(waittime)
        return self

    def input(self,content,waittime=None):
        '''
        Sends the characters contained in message to this device, as if they had been typed on the device's 
        keyboard. This is equivalent to calling press() for each keycode in message using the key event type 
        DOWN_AND_UP.

        @type content: string
        @param content: A string containing the characters to send. 
        @type waittime: int
        @param waittime: The idle time after input action. Default value is len(content)*1/3*0.5 seconds. See "runner/stability/sysconfig"
        @rtype: device object
        @return: The instance of device object. 
        '''
        self.impl.typeWord(content)
        if not waittime:
            defaulttime = int(self.config.get('time','after_input_time'))
            waittime = len(content)*defaulttime/3
        self.impl.sleep(waittime)
        return self

    def drag(self,start,end,time,steps,waittime=None):
        '''
        Simulates a drag gesture (touch, hold, and move) on this device's screen.

        @type start: tuple
        @param start: The starting point of the drag gesture, in the form of a tuple (x,y) where x and y are integers.
        @type end: tuple  
        @param end: The end point of the drag gesture, in the form of a tuple (x,y) where x and y are integers.
        @type time: int
        @param time: The duration of the drag gesture in seconds. The default is 1.0 seconds.
        @type steps: int
        @param steps: The number of steps to take when interpolating points. The default is 10.   
        @type waittime: int
        @param waittime: The idle time after drag action. Default value is 1 seconds. See "runner/stability/sysconfig"
        @rtype: device object
        @return: The instance of device object. 
        '''
        self.impl.drag(start,end,time,steps)
        if not waittime:
            waittime = int(self.config.get('time','after_drag_time'))
        self.impl.sleep(waittime)
        return self

    def sleep(self,seconds):
        '''
        Pauses the current program for the specified number of seconds.

        @type seconds: int
        @param seconds: The number of seconds to pause.
        @rtype: device object
        @return: The instance of device object. 
        '''
        self.impl.sleep(seconds)
        return self

    def adbCmd(self,command,waittime=None):
        '''
        Executes an adb shell command and returns the result, if any. 

        @type command: string
        @param command: The command to execute in the adb shell. 
        @type waittime: int
        @param waittime:The idle time after shell command action. Default value is 2 seconds. See "runner/stability/sysconfig"
        @rtype: device object
        @return: The instance of device object. 
        '''
        response = self.impl.adbcommand(command)
        if not waittime:
            waittime = int(self.config.get('time','after_shellcmd_time'))
        self.impl.sleep(waittime)
        return response

    def adbCmdNoReturn(self,command,waittime=None):
        '''
        Executes an adb shell command and don't returns the result.

        @type command: string
        @param command: The command to execute in the adb shell. 
        @type waittime: int
        @param waittime:The idle time after shell command action. Default value is 2 seconds. See "runner/stability/sysconfig"
        '''
        self.impl.adbcommand(command)
        if not waittime:
            waittime = int(self.config.get('time','after_shellcmd_time'))
        self.impl.sleep(waittime)
        return self

class TestCheck:
    '''
    Interface for invoking test verify.
    '''
    def setChecker(self,testChecker):
        '''
        Set the instance of test checker.
        @param checker 
        @type Instance of Checker.
        '''
        self.checkpoint = -1
        self.checker = testChecker

    def expect(self,name=None,interval=None,timeout=None):
        '''
        Check weather the expected image is contained in the current screen snapshot.if contained pass otherwise thrown exception.
        @type name: string
        @param name The ex: ected image(png) file name.
        @type interval: int
        @param interval: The interval time after one check. Default value is 3 seconds.
        @type timeout: int
        @param timeout: The duration time of waitting the screen snapshot. Default value is 9 seconds. See "runner/stability/sysconfig"
        @type int
        @rtype: Device object or Exception
        @return: If pass return the instance of device. otherwise throw exception and set the test result to be failure.
        '''
        if not interval:
            interval = int(self.config.get('time','expect_interval_time'))
        if not timeout:
            timeout = int(self.config.get('time','expect_timeout'))
        self.checker.expect(name,interval=interval,timeout=timeout)
        return self

    def exists(self,name=None,interval=None,timeout=None):
        '''
        Check weather the ecpected image is contained in the current screen snpshot. If contained return True otherwise return False 
        
        @type name: string
        @param name: The expected image(png) file name.
        @type interval: int
        @param interval: The interval time after one check. Default value is 2 seconds.
        @type timeout: int
        @param timeout: The time of waitting the screen snapshot.default value is 4 seconds. See "runner/stability/sysconfig"
        @rtype: boolean
        @return: If exists return True. If doesen't exists return Fail.
        '''
        if not interval:
            interval = int(self.config.get('time','exists_interval_time'))
        if not timeout:
            timeout = int(self.config.get('time','exists_timeout'))
        return self.checker.exists(name,interval=interval,timeout=timeout)

class Checker(object):

    def __init__(self,options=None,deviceImpl=None,output=None,expect=None):
        self.logger = Logger.getLogger()
        self.option = options
        self.device = deviceImpl
        self.testResult = output
        self.expectResult = expect
        self._checkpoint = -1

    def expect(self,fname,interval,timeout):
        self.logger.debug('Check curren screen...')
        path = self.testResult.dirs['all']
        tag = '.png'

        if (fname == None):
            self._checkpoint = self._checkpoint + 1
            names = self.__basename(str(self._checkpoint)+'.wait')['snapshot']
        else:
            if fname.find(tag):
                fname = fname.replace(tag,'')
            check_region = self.expectResult.getCurrentPath(fname)
            ##names = '%s.snapshot.png' % fname
            right_snapshot = self.expectResult.getCurrentCheckPointParent()
            dirs,filename = os.path.split(right_snapshot)
            rect = filename.split('.')[1]
            names = '%s.%s.png' % (fname,rect)
            self.logger.debug('check name:')
            self.logger.debug(names)

        device_snapshot = os.path.join(path, names)

        begin = time.time()
        while (time.time() - begin < timeout):
            self.logger.debug('interval time wait>>>')
            time.sleep(interval)
            self.capture(device_snapshot,upload=True)
            if imglib.isRegionMatch(device_snapshot,check_region):
                return self
        assert False,'assert fail: Timeout during checking screen snapshot'

    def exists(self,fname,interval,timeout):
        device_snapshot,check_region = self.__comparePath(fname)
        begin = time.time()
        isExists = False
        while (time.time() - begin < timeout):
            time.sleep(interval)
            self.capture(device_snapshot)
            isExists = imglib.isRegionMatch(device_snapshot,check_region)
            if not isExists:
                continue
        return isExists

    def capture(self,name,upload=False):
        r = self.device.takeSnapshot()
        r.writeToFile(name, 'png')
        if upload:
            pub.sendMessage('collectresult',path=name)

    def __comparePath(self,name=None):
        self.logger.debug('check--NAME--check')
        path = self.testResult.dirs['all']
        tag = '.png'
        if (name == None):
            self._checkpoint = self._checkpoint + 1
            names = self.__basename(str(self._checkpoint)+'.wait')['snapshot']
        else:
            if name.find(tag):
                name = name.replace(tag,'')
            check_region = self.expectResult.getCurrentPath(name)
            self.logger.debug(check_region)
            #names = '%s.snapshot.png' % name
            #add 1120
            right_snapshot = self.expectResult.getCurrentCheckPointParent()
            dirs,filename = os.path.split(right_snapshot)
            rect = filename.split('.')[1]

            names = '%s.%s.png' % (name,rect)
            self.logger.debug('check name>>>>>>>>')
            self.logger.debug(names)

        device_snapshot = os.path.join(path, names)
        return [device_snapshot,check_region]


    def __basename(self, name):
        names = {}
        names['snapshot'] = '%s.snapshot.png' % name
        names['checkpoint'] = '%s.checkpoint.png' % name
        names['ocr'] = '%s.ocr.txt' % name
        return names

class testWorker(TestAction,TestCheck):
    """
    Provides the executing ability of each TestCase.
    """
    def __init__(self, options=None):
        self.logger = Logger.getLogger()
        self.option = options
        self.config = ConfigParser.ConfigParser()
        self.config.read(os.path.join('%s%s%s' % (os.path.dirname(os.path.dirname(__file__)),os.sep,'sysconfig')))

    def __mixIn(self,pyClass,mixInClass):
        if mixInClass not in pyClass.__bases__:
            pyClass.__bases__ = (mixInClass,) + pyClass.__bases__

    def run(self,test,outputResult):
        self.logger.debug('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>init device<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        device = DeviceManager.getInstance().getDevice()
        case_name = '%s.%s' %(type( test).__name__,  test._testMethodName)
        class_name = test.__module__.split('.')[2]
        expectResultPath = os.path.join(outputResult.dirs['ws_right'],'%s.%s' % (class_name,case_name))
        self.logger.debug('expect result path:')
        self.logger.debug(expectResultPath)
        expectResult = ExpectResult(expectResultPath)
        checker = Checker(self.option,device,outputResult,expectResult)
        self.__mixIn(unittest.TestCase,testWorker)
        if isinstance(test,unittest.TestCase):
            test.setDeviceImpl(device,self.config)
            test.setChecker(checker)
            test.logger = self.logger
            test(outputResult)

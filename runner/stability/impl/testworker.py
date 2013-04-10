#!/usr/bin/env python  
#coding: utf-8
'''
Module provides API to interact with device and verify the check ponit.
It provides:
Action class to define the interface interact with target device.
Verify class to define the interface for checking checkpoint.
Verifer class to implement the Verify interface.
TestWorker class to run a test case.
@version: 1.0
@author: borqsat
@see: null
'''

import time,sys,os,shutil,datetime,string,unittest
from devicemanager import DeviceManager
from expectresult import ExpectResult
from stability.util.log import Logger
from libs.pubsub import pub
from libs.imglib import imglib
from configparser import Parser

class Action:
    '''
    Interface for sending test action.
    '''
    def setActionImpl(self,deviceImpl):
        '''
        Set the instance of device implement.
        @type deviceImpl: Object of device.
        @param deviceImpl: Instance of device.
        '''
        self.device = deviceImpl

    def launch(self,component=None,flags=0x04000000,data=None,action=None,uri=None,mimetype=None,categories=None,extras=None,waittime=None):
        '''
        Starts an App on device by sending an Intent constructed from the supplied arguments.
        Also you can start an Activity by touching the icon of APP on home screen.

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
        @type mimetype: String
        @param mimetype: The MIME type for the Intent.
        @type categories: String
        @param categories: An iterable data structure containing strings that define categories for the Intent.
        @type extras: String
        @param extras: A dictionary of extra data for the Intent.
        @type waittime: Int
        @param waittime: The idle time after launching activity. The default value is 3 seconds. See "runner/stability/sysconfig"
        @rtype: unittest.TestCase
        @return: a instance of unittest.TestCase which have the ability to interact with device and verify the checkpoint
        '''
        self.device.startActivity(component, flags,data,action,uri,mimetype,categories,extras)
        if not waittime and waittime != 0:
            #waittime = int(self.config.get('time','after_launch_time'))
            waittime = int(self.config.after_launch_time)
        self.device.sleep(waittime)
        return self
    
    def press(self,keyseq,waittime=None):
        '''
        Sends the key event sequence specified by type to the key specified by keycode.
        Like:'home,menu,back,up,down,left,right,center'
        @type keyseq: string
        @param keyseq: The key event sequence string split by character ','.
        @type waittime: int
        @param waittime: The idle time after press action. Default is 1 seconds after one key action. See "runner/stability/sysconfig"
        @rtype: unittest.TestCase
        @return: a instance of unittest.TestCase which have the ability to interact with device and verify the checkpoint
        '''
        if not waittime and waittime != 0:
            waittime = int(self.config.after_press_time)
        self.device.pressKey(keyseq,interval=waittime)
        return self

    def touch(self,arg,similarity=0.7,waittime=None):
        '''
        Perform a touch event on the touch point or on the screen region.
        The touch point specified by type to the screen location specified by x and y.
        If the screen region want to touch not found in the current screen snapshot will throw exception.

        @type arg: string
        @param arg: 
        String : a image file path which contained in the current device's scrren.
        @type arg: tuple
        @param arg: 
        The screen location specified by x and y.
        Format: (x,y) the screen location specified by x and y.
        x   The horizontal position of the touch in actual device pixels, starting from the left of the screen in its current orientation.
        y   The vertical position of the touch in actual device pixels, starting from the top of the screen in its current orientation.
        @type similarity:float
        @param similarity: The minimum similarity a match should have. If omitted, the default is used
        @type waittime: int
        @param waittime: The idle time after touch action. Default value is 1 seconds. See "runner/stability/sysconfig"
        @rtype: unittest.TestCase
        @return: a instance of unittest.TestCase which have the ability to interact with device and verify the checkpoint
        '''
        if not waittime and waittime != 0:
            waittime = int(self.config.after_touch_time)
        if isinstance(arg,str):
            path =  self.verifier.testResult.dirs['all']
            #add 1120
            if arg.find('.png'):
                arg = arg.replace('.png','')

            smallSnapshot = self.verifier.expectResult.getCurrentPath(arg)
            ###names = '%s.snapshot.png' % arg
            right_snapshot = self.verifier.expectResult.getCurrentCheckPointParent()
            dirs,filename = os.path.split(right_snapshot)
            rect = filename.split('.')[1]
            names = '%s.%s.png' % (arg,rect)
            largeSnapshot = os.path.join(path, names)
            success = self.verifier.capture(largeSnapshot)
            point = None
            if success:
                point = imglib.getRegionCenterPoint(src=largeSnapshot,sub=smallSnapshot,similarity=similarity)
            if not point:
                #fail_reason = 'Cant find the expected image %s from %s ' % (smallSnapshot,largeSnapshot)
                fail_reason = 'Failure reason: Image \'%s\' can not be found on screen!' % os.path.basename(smallSnapshot)
                self.verifier.upload(largeSnapshot)
                assert False,fail_reason
            self.verifier.upload(largeSnapshot)
            self.device.touch(int(point[0]),int(point[1]))
            self.logger.debug('touch picture:(%s,%s)' % (str(point[0]),str(point[1])))
        elif isinstance(arg,tuple):
            self.device.touch(arg[0],arg[1])
            self.logger.debug('touch point:(%s,%s)' % (str(arg[0]),str(arg[1])))
        self.device.sleep(waittime)
        return self

    def longtouch(self,arg,similarity=0.7,waittime=None):
        '''
        Perform a long touch event on the touch point or on the screen region.
        The touch point specified by type to the screen location specified by x and y.
        If the screen region want to touch not found in the current screen snapshot will throw exception.


        @type arg: string
        @param arg: 
        String : a image file path which contained in the current device's scrren 
        @type arg: touple
        @param arg: 
        The screen location specified by x and y.
        Format: (x,y) the screen location specified by x and y.
        x   The horizontal position of the touch in actual device pixels, starting from the left of the screen in its current orientation.
        y   The vertical position of the touch in actual device pixels, starting from the top of the screen in its current orientation.
        @type waittime: int
        @param waittime: The idle time after touch action. Default value is 1 seconds. See "runner/stability/sysconfig"
        @type similarity:float
        @param similarity: The minimum similarity a match should have. If omitted, the default is used
        @rtype: unittest.TestCase
        @return: a instance of unittest.TestCase which have the ability to interact with device and verify the checkpoint
        '''
        if not waittime and waittime != 0:
            waittime = int(self.config.after_touch_time)
        if isinstance(arg,str):
            path =  self.verifier.testResult.dirs['all']
            #add 1120
            if arg.find('.png'):
                arg = arg.replace('.png','')

            smallSnapshot = self.verifier.expectResult.getCurrentPath(arg)
            ###names = '%s.snapshot.png' % arg
            right_snapshot = self.verifier.expectResult.getCurrentCheckPointParent()
            dirs,filename = os.path.split(right_snapshot)
            rect = filename.split('.')[1]
            names = '%s.%s.png' % (arg,rect)
            largeSnapshot = os.path.join(path, names)
            success = self.verifier.capture(largeSnapshot)
            point = None
            if success:
                point = imglib.getRegionCenterPoint(largeSnapshot,smallSnapshot,similarity=similarity)
            if not point:
                #fail_reason = 'Can find the matched image %s from %s ' % (smallSnapshot,largeSnapshot)
                fail_reason = 'Failure reason: Image \'%s\' can not be found on screen!' % os.path.basename(smallSnapshot)
                self.verifier.upload(largeSnapshot)
                assert False,fail_reason
            self.verifier.upload(largeSnapshot)
            #long touch
            x = int(point[0])
            y = int(point[1])
            time = 4
            steps = 6
            self.device.drag((x,y),(x,y),time,steps)
            ##self.device.touch(int(point[0]),int(point[1]))
            self.logger.debug('action: long touch picture -> (%s,%s)' % (str(point[0]),str(point[1])))
        elif isinstance(arg,tuple):
            x = arg[0]
            y = arg[1]
            time = 4
            steps = 6
            self.device.drag((x,y),(x,y),time,steps)
            self.logger.debug('action: long touch point -> (%s,%s)' % (str(arg[0]),str(arg[1])))
        self.device.sleep(waittime)
        return self

    def input(self,content,waittime=None):
        '''
        Type the text at the current device's screen focused input field 
        The content the characters contained in message to this device, as if they had been typed on the device's 
        keyboard. This is equivalent to calling press() for each keycode in message using the key event type 
        DOWN_AND_UP.

        @type content: string
        @param content: A string containing the characters to send. as if they had been typed on the device's keyboard.
        @type waittime: int
        @param waittime: The idle time after input action. Default value is len(content)*1/3*0.5 seconds. See "runner/stability/sysconfig"
        @rtype: unittest.TestCase
        @return: a instance of unittest.TestCase which have the ability to interact with device and verify the checkpoint
        '''
        self.device.typeWord(content)
        if not waittime and waittime != 0:
            defaulttime = int(self.config.after_input_time)
            waittime = len(content)*defaulttime/3
        self.device.sleep(waittime)
        return self

    def drag(self,start,end,time,steps,waittime=None):
        '''
        Perform a drag-and-drop operation by dragging at the given click point.
        Used to simulate a drag gesture (touch, hold, and move) on this device's screen.

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
        @rtype: unittest.TestCase
        @return: a instance of unittest.TestCase which have the ability to interact with device and verify the checkpoint
        '''
        self.device.drag(start,end,time,steps)
        if not waittime and waittime != 0:
            waittime = int(self.config.after_drag_time)
        self.device.sleep(waittime)
        return self

    def sleep(self,seconds):
        '''
        Pauses the current program for the specified number of seconds.

        @type seconds: int
        @param seconds: The number of seconds to pause.
        @rtype: unittest.TestCase
        @return: a instance of unittest.TestCase which have the ability to interact with device and verify the checkpoint
        '''
        self.device.sleep(seconds)
        return self

    def adbCmd(self,command,waittime=None):
        '''
        Executes an adb shell command and returns the result, if any. 

        @type command: string
        @param command: The command to execute in the adb shell. 
        @type waittime: int
        @param waittime:The idle time after shell command action. Default value is 2 seconds. See "runner/stability/sysconfig"
        @rtype: string
        @return: the device shell output
        '''
        response = self.device.adbcommand(command)
        if not waittime and waittime != 0:
            waittime = int(self.config.after_shellcmd_time)
        self.device.sleep(waittime)
        return response

    def adbCmdNoReturn(self,command,waittime=None):
        '''
        Executes an adb shell command and don't returns the result.

        @type command: string
        @param command: The command to execute in the adb shell.
        @type waittime: int
        @param waittime:The idle time after shell command action. Default value is 2 seconds. See "runner/stability/sysconfig"
        @rtype: unittest.TestCase
        @return: a instance of unittest.TestCase which have the ability to interact with device and verify the checkpoint       
        '''
        self.device.adbcommand(command)
        if not waittime and waittime != 0:
            waittime = int(self.config.after_shellcmd_time)
        self.device.sleep(waittime)
        return self

class Verify:
    '''
    Interface for invoking test verify.
    '''
    def setVerifyImpl(self,testVerifier):
        '''
        Set the instance of test verifier.
        @type testVerifier: object of Verify.
        @param testVerifier: instance of Verify object.
        '''
        self.checkpoint = -1
        self.verifier = testVerifier

    def expect(self,name=None,interval=None,timeout=None,similarity=0.7,msg=None):
        '''
        Allows to search for a expected image in an image file that you provide (e.g. a screenshot taken and saved in a file before)
        Check whether the expected image was found that satisfy the minimum similarity requirement. If found return self,
        if not found will throw exception then test case failed 
        @type name: string
        @param name: The expected image(png) file name.
        @type interval: int
        @param interval: The interval time after one check. Default value is 3 seconds.
        @type timeout: int
        @param timeout: The duration time of waitting the screen snapshot. Default value is 9 seconds. See "runner/stability/sysconfig"
        @type similarity:float
        @param similarity: The minimum similarity a match should have. If omitted, the default is used
        @type msg:string
        @param msg: Output string if the expected image not found in the target image file. 
        @rtype: unittest.TestCase
        @return: a instance of unittest.TestCase which have the ability to interact with device and verify the checkpoint
        '''
        if not interval and interval != 0:
            interval = int(self.config.expect_interval_time)
        if not timeout and timeout != 0:
            timeout = int(self.config.expect_timeout)
        self.verifier.expect(name,interval=interval,timeout=timeout,similarity=similarity,msg=msg)
        return self

    def exists(self,name=None,interval=None,timeout=None,similarity=0.7):
        '''
        Check whether the expected image was found that satisfy the minimum similarity requirement. If found return True, 
        If not found return False.
        @type name: string
        @param name: The expected image(png) file name.
        @type interval: int
        @param interval: The interval time after one check. Default value is 2 seconds.
        @type timeout: int
        @param timeout: The time of waitting the screen snapshot.default value is 4 seconds. See "runner/stability/sysconfig"
        @type similarity:float
        @param similarity: The minimum similarity a match should have. If omitted, the default is used
        @rtype: boolean
        @return: return ture if the expect check point exists in screen. false if not exists.
        '''
        if not interval and interval != 0:
            interval = int(self.config.exists_interval_time)
        if not timeout and timeout != 0:
            timeout = int(self.config.exists_timeout)
        return self.verifier.exists(name,interval=interval,timeout=timeout,similarity=similarity)

class Verifier(Verify):
    '''
    A class that implments Verify interface.
    '''
    def __init__(self,options=None,deviceImpl=None,output=None,expect=None):
        '''
        init the verifier instance with current session properties.
        @type options: dictionary
        @param options: user input properties
        @type deviceImpl: device.Device
        @param deviceImpl: the target device instance
        @type output: testrunner._TestResult
        @param output: a instance of _TestResult which maintain the test tesult
        @type expect: expectresult.ExpectResult
        @param expect: a instance of ExpectResult which maintain the  snapshot collection of current test case    
        '''
        self.logger = Logger.getLogger()
        self.option = options
        self.device = deviceImpl
        self.testResult = output
        self.expectResult = expect
        self._checkpoint = -1

    def expect(self,fname,interval,timeout,similarity,msg):
        '''
        Verify the snapshot of check point.
        Allows to search for a expected image in an image file that you provide (e.g. a screenshot taken and saved in a file before)
        Check whether the expected image was found that satisfy the minimum similarity requirement. If found return self,
        if not found will throw exception then test case failed.    
        '''
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
            self.logger.debug('%s %s' % ('expect snapshot : ',names))

        device_snapshot = os.path.join(path, names)

        begin = time.time()
        while (time.time() - begin < timeout):
            self.logger.debug('wait interval time')
            time.sleep(interval)
            success = self.capture(device_snapshot)
            if success and imglib.isRegionMatch(src=device_snapshot,sub=check_region,similarity=similarity):
                self.upload(device_snapshot)
                return self
        self.upload(device_snapshot)
        if not msg:
            fail_reason = 'Fail Reason: Image \'%s\' cant not be found on screen!' % os.path.basename(check_region)
        else:
            fail_reason = msg
        assert False,fail_reason

    def exists(self,fname,interval,timeout,similarity):
        '''
        Check whether the expected image was found that satisfy the minimum similarity requirement. If found return True, 
        If not found return False.
        '''
        device_snapshot,check_region = self.__comparePath(fname)
        begin = time.time()
        isExists = False
        while (time.time() - begin < timeout):
            time.sleep(interval)
            success = self.capture(device_snapshot)
            if success:
                isExists = imglib.isRegionMatch(src=device_snapshot,sub=check_region,similarity=similarity)
                self.logger.debug('check wheather %s exists in %s ' % (check_region,device_snapshot))
            if not isExists:
                continue
        self.logger.debug('exists: %s' % isExists)
        return isExists

    def capture(self,name):
        '''
        Capture snapshot from current device screen.
        @type name: string
        @param name: the save path of snapshot
        @rtype: boolean
        @return: true if capture completed. false if capture error.
        '''
        ret = False
        try:
            ret = self.device.takeSnapshot(name)
        except:
            ret = False
        finally:
            return ret

    def upload(self,name):
        '''
        Upload the snapshot to server.
        @type name: string
        @param name: the save path of snapshot        
        '''
        pub.sendMessage('collectresult',path=name)

    def __comparePath(self,name=None):
        '''
        Get the full snapshot path and check point snapshot path.
        @type name: string
        @param name: the path of check point snapshot
        @rtype: list
        @return: a list of full snapshot path and check point snapshot path
        '''
        path = self.testResult.dirs['all']
        tag = '.png'
        if (name == None):
            self._checkpoint = self._checkpoint + 1
            names = self.__basename(str(self._checkpoint)+'.wait')['snapshot']
        else:
            if name.find(tag):
                name = name.replace(tag,'')
            check_region = self.expectResult.getCurrentPath(name)
            right_snapshot = self.expectResult.getCurrentCheckPointParent()
            dirs,filename = os.path.split(right_snapshot)
            rect = filename.split('.')[1]

            names = '%s.%s.png' % (name,rect)
            self.logger.debug('%s %s' % ('expect snapshot : ',names))

        device_snapshot = os.path.join(path, names)
        return [device_snapshot,check_region]


    def __basename(self, name):
        '''
        Generate the snapshot file name.Not used now.
        '''
        names = {}
        names['snapshot'] = '%s.snapshot.png' % name
        names['checkpoint'] = '%s.checkpoint.png' % name
        names['ocr'] = '%s.ocr.txt' % name
        return names

class TestWorker(Action,Verify):
    '''
    Provides the executing ability of each TestCase.
    '''
    def __init__(self, options=None):
        '''
        init instance of TestWorker.
        @type options: dictionary
        @param options: user input properties
        '''
        self.logger = Logger.getLogger()
        self.option = options
        self.systemConfig = Parser.getSystemConfig()

    def __mixIn(self,pyClass,mixInClass):
        '''
        Mix the real ability to target object instance.
        '''
        if mixInClass not in pyClass.__bases__:
            pyClass.__bases__ = (mixInClass,) + pyClass.__bases__

    def run(self,test,outputResult):
        self.logger.debug('>>>>>>>>>>>>>>>>>>>>>>>worker run<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        device = DeviceManager.getInstance().getDevice()
        case_name = '%s.%s' %(type( test).__name__,  test._testMethodName)
        class_name = test.__module__.split('.')[2]
        expectResultPath = os.path.join(outputResult.dirs['ws_right'],'%s.%s' % (class_name,case_name))
        self.logger.debug('%s %s' % ('expect resource path:',expectResultPath))
        expectResult = ExpectResult(expectResultPath)
        verifier = Verifier(self.option,device,outputResult,expectResult)
        if isinstance(test,unittest.TestCase):
            self.__mixIn(unittest.TestCase,TestWorker)
            test.setActionImpl(device)
            test.setVerifyImpl(verifier)
            test.logger = self.logger
            test.config = self.systemConfig
            test(outputResult)

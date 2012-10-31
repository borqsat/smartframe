#!/usr/bin/env python
import time, sys, os, shutil, datetime, string
from stability.util.log import Logger
from devicemanager import DeviceManager
import unittest
from expectresult import ExpectResult
from imglib import imglib
from listener import collectSnapshot

class TestAction:
    '''
    Interface for sending test action.
    '''
    def setDeviceImpl(self,deviceImpl,result=None):
        '''
        Set the instance of device implement.
        @param deviceImpl 
        @type Instance of device.
        '''
        self.impl = deviceImpl

    def launch(self, component=None, flags=0x04000000):
        '''
        Starts an Application on this device by sending an Intent constructed from the supplied arguments.
        @param  component
        The component for the Intent . Using this argument will direct the Intent to a specific class within 
        a specific Android package. 
        @type string
        @param flags
        An iterable data structure containing flags that control how the Intent is handled
        @type: int
        '''
        self.impl.startActivity(component,flags)
        return self
    
    def press(self,keyseq):
        '''
        Sends the key event sequence specified by type to the key specified by keycode. 
        @param  keyseq
        The component for the Intent . Using this argument will direct the Intent to a specific class within 
        a specific Android package. 
        @type string -- a string seperate by character ','
        '''
        self.impl.pressKey(keyseq)
        return self

    def touch(self,arg):
        '''
        Sends a touch event to the device's scrren region or specified by type to the screen location specified 
        by x and y. 
        @param arg
        a image file path which contained in the current device's scrren or the screen location specified by x and y.
        @type string -- a image file path
               tuple(x,y) the screen location specified by x and y.
               x   The horizontal position of the touch in actual device pixels, starting from the left of the screen in its current orientation.
               y   The vertical position of the touch in actual device pixels, starting from the top of the screen in its current orientation. 
        '''
        if isinstance(arg,str):
            path =  self.checker.testResult.dirs['all']
            names = '%s.snapshot.png' % arg
            largeSnapshot = os.path.join(path, names)
            self.checker.capture(largeSnapshot)
            smallSnapshot = self.checker.expectResult.getCurrentPath(arg)
            point = imglib.getRegionCenterPoint(largeSnapshot,smallSnapshot)
            if not point:
                assert False,'Can find the matched image %s from %s ' % (smallSnapshot,largeSnapshot)
            self.impl.touch(int(point[0]),int(point[1]))
        else:
            self.impl.touch(arg[0],arg[1])
        return self

    def input(self,content):
        '''
        Sends the characters contained in message to this device, as if they had been typed on the device's 
        keyboard. This is equivalent to calling press() for each keycode in message using the key event type 
        DOWN_AND_UP. 
        @param content
        A string containing the characters to send. 
        @type string
        '''
        self.impl.typeWord(content)
        return self

    def drag(self,start,end,time,steps):
        '''
        Simulates a drag gesture (touch, hold, and move) on this device's screen.
        @param: 
        start   The starting point of the drag gesture, in the form of a tuple (x,y) where x and y are integers.
        end     The end point of the drag gesture, in the form of a tuple (x,y) where x and y are integers.
        duration    The duration of the drag gesture in seconds. The default is 1.0 seconds.
        steps   The number of steps to take when interpolating points. The default is 10.
        '''
        self.impl.drag(start,end,time,steps)
        return self

    def sleep(self,seconds):
        '''
        Pauses the current program for the specified number of seconds.
        @param seconds
        The number of seconds to pause. 
        @type float
        '''
        self.impl.sleep(seconds)
        return self

    def adbCmd(self,command):
        '''
        Executes an adb shell command and returns the result, if any. 
        @param command
        The command to execute in the adb shell. 
        @type string
        '''
        self.impl.adbcommand(command)
        return self

class TestCheck:
    '''
    Interface for invoking test verify.
    '''
    def setChecker(self,checker):
        '''
        Set the instance of test checker.
        @param checker 
        @type Instance of Checker.
        '''
        self.checkpoint = -1
        self.checker = checker

    def waitForScreen(self,name=None, timeout=10, rect=(0, 0, 1, 1), th=0.7):
        '''
        Test verify method.Check the ecpected screen is shown. if shown pass else thown exception. 
        @param name
        screen snaoshot name
        @type string
        @param timeout
        the duration time of waitting
        @type int
        @param rect
        the expected rectangle of screen
        @type tuple
        @param th
        the expected similartity
        @type float
        '''
        self.checker.waitForScreen(name,timeout,rect,th)
        return self

    def waitForString(self):
        '''
        Test verify method.
        Check weather the ecpected string is contained in the current screen snpshot.Not support yet.
        '''
        return self
    
    def expect(self,name=None,timeout=2):
        '''
        Test verify method.
        Check weather the ecpected image is contained in the current screen snpshot. 
        if contained pass otherwise thown exception. 
        @param name
        The expected image(png) file path.
        @type string
        @param timeout
        The time of waitting the screen snapshot.default value is 2 seconds.
        @type int
        '''
        self.checker.check(name,timeout)
        return self

    def exists(self,name=None,timeout=2):
        '''
        Test verify method.
        Check weather the ecpected image is contained in the current screen snpshot. 
        if contained return True otherwise return False 
        @param name
        The expected image(png) file path.
        @type string
        @param timeout
        The time of waitting the screen snapshot.default value is 3 seconds.
        @type int
        '''
        return self.checker.exists(name,timeout)

class Checker(object):

    def __init__(self,options=None,deviceImpl=None,output=None,expect=None):
        self.logger = Logger.getLogger()
        self.option = options
        self.device = deviceImpl
        self.testResult = output
        self.expectResult = expect
        self._checkpoint = -1

    def check(self,fname,timeout):
        self.logger.debug('check time out')
        self.logger.debug(timeout)
        self.logger.debug('Check curren screen.')
        check_region = self.expectResult.getCurrentPath(fname)
        path = self.testResult.dirs['all']
        if (fname == None):
            self._checkpoint = self._checkpoint + 1
            names = self.basename(str(self._checkpoint)+'.wait')['snapshot']
        else:
            names = '%s.snapshot.png' % fname

        device_snapshot = os.path.join(path, names)

        begin = time.time()
        while (time.time() - begin < timeout):
            self.logger.debug('timeout loop>>')
            self.capture(device_snapshot)
            if imglib.isRegionMatch(device_snapshot,check_region):
                return self
        assert False,'assert fail: Timeout during checking screen snapshot'

    def exists(self,fname,timeout):
        device_snapshot,check_region = self.__comparePath(fname)
        begin = time.time()
        isExists = False
        while (time.time() - begin < timeout):
            self.capture(device_snapshot)
            isExists = imglib.isRegionMatch(device_snapshot,check_region)
            if not isExists:
                continue
        return isExists

    @collectSnapshot
    def capture(self,name):
        r = self.device.takeSnapshot()
        r.writeToFile(name, 'png')

    def __comparePath(self,name=None):
        check_region = self.expectResult.getCurrentPath(name)
        self.logger.debug('check--NAME--check')
        self.logger.debug(check_region)
        path = self.testResult.dirs['all']
        if (name == None):
            self._checkpoint = self._checkpoint + 1
            names = self.basename(str(self._checkpoint)+'.wait')['snapshot']
        else:
            names = '%s.snapshot.png' % name

        device_snapshot = os.path.join(path, names)
        
        self.capture(device_snapshot)
        return [device_snapshot,check_region]

    def waitForScreen(self, name=None, timeout=10, rect=(0, 0, 1, 1), th=0.7):
        self.logger.debug('Enter waitForScreen.')
        if (name == None):
            self._checkpoint += 1
            name = str(self._checkpoint) + '.wait'
        else:
            assert self.__isValidName(name),'Invalid checkpoint name: %s.' % name
        if self.option['recording']:
            #recording
            self.logger.debug('Recording >>> Wait for %d seconds and then save snapshot as standard picture.'%timeout)
            #If recording should diff should be 0
            assert self.checkImage(name, rect) == 0

        else:
            # testing
            self.logger.debug('Testing >>> Waiting for screen...')
            begin = time.time()
            while (time.time() - begin < timeout):
                self.logger.debug('Elapsed %f seconds...'% (time.time() - begin))
                diff = self.checkImage(name, rect)
                self.logger.debug('diff rate :' + str(diff)+'\n')
                if (diff >= 0 and diff <= th):
                    self.logger.debug('Reach the waiting screen.')
                    #return True
                    assert True,'assert pass: Timeout during waitForScreen'
                    return self
            self.logger.debug('Timeout during waitForScreen.')
            assert False,'assert fail: Timeout during waitForScreen'
        return self            

    def checkImage(self, name=None, rect=(0, 0, 1, 1)):
        """
        Check snapshot in specified rect and return the diff rate from standard one.
        (0,0,1,1) means the whole screen.
        """
        if (name == None):
            self._checkpoint += 1
            name = str(self._checkpoint) + '.check'
        else:
            assert self.__isValidName(name),'Invalid checkpoint name: %s.' % name
        assert rect is not None
        self.saveImage(name, rect)
        diff = 0
        if not self.option['recording']: # not recording, so we should compare the image.
            self.logger.debug("Not recording, so it's a checkpoint.")
            names = self.basename(name)
            #sys.stderr.write(str(os.path.exists(os.path.join(self.workspace_result_right, names['checkpoint']))))
            filename_right = os.path.join(self.testResult.dirs['right'], names['checkpoint'])
            filename = os.path.join(self.testResult.dirs['all'], names['checkpoint'])
            #self.assertTrue(os.path.exists(filename_right) and os.path.exists(filename))
            assert os.path.exists(filename_right),'file does not exists %s '% filename_right
            assert os.path.exists(filename),'file does not exists %s '% filename
            # Compare the two images
            diff = self._compare(filename, filename_right)
            self.logger.debug("The diff at checkpoint %s is %f."%(name, diff))
        return diff

    def saveImage(self, name=None, rect=None, ocr=False):
        "Save the snapshot."
        if (name == None):
            self._checkpoint += 1
            name = str(self._checkpoint) + '.save'
        else:
            assert self.__isValidName(name),'Invalid checkpoint name: %s.' % name

        self.logger.debug('Save snapshot at checkpoint: %s.' % name)
        if self.option['recording']:
            path = self.testResult.dirs['right']
        elif self.option['testing']:
            path = self.testResult.dirs['all']

        names = self.basename(name)

        filename_snapshot = os.path.join(path, names['snapshot'])

        filename_checkpoint = os.path.join(path, names['checkpoint'])
        #filename_ocr = os.path.join(path, names['ocr'])   
        rect_screen = rect and self.device.convert_to_screen_rect(rect)

        self.capture(filename_snapshot)# snapshot
        #here ResultSender will upload snapshot to server by sid or tid
        #from handler import ResultSender
        #ResultSender.getInstance.addTask(path=filename_snapshot)
        if rect_screen is not None: # save subimage (checkpoint)
            r.getSubImage(rect_screen).writeToFile(filename_checkpoint, 'png')

    def _compare(self, f1, f2):
        "Compare the two images in the two files: f1 and f2."
        #TODO: subprocess.Popen leaks fds, so...
        #proc = subprocess.Popen(['python', os.path.join(self.stability_home, 'compare.py'), f1, f2], stdout=subprocess.PIPE)
        #proc.wait()
        #r = proc.communicate()[0]
        import commands
        cmd = '%s %s %s %s' % ('python', os.path.join(os.path.dirname(__file__), 'compare.py'), f1, f2)
        r = commands.getoutput(cmd)
        return float(r)
        
    def _exists(self,full,sub):
        pass

    def basename(self, name):
        names = {}
        names['snapshot'] = '%s.snapshot.png' % name
        names['checkpoint'] = '%s.checkpoint.png' % name
        names['ocr'] = '%s.ocr.txt' % name
        return names

    def __isValidName(self, name):
        """
        Check if the name is valid.
        The name should only contain string.ascii_leters, string.digits, '-',
        '_' and '.', and it must be prefixed by string.ascii_leters
        """
        valid = string.ascii_letters + string.digits + '-' + '_' + '.'
        if (name == None or len(name) == 0):
            return False
        for c in name:
            if (string.find(valid, c) == -1):
                return False
        if (string.find(string.ascii_letters, name[0]) == -1
            and string.find(string.digits, name[0]) == -1):
            return False
        return True

class testWorker(TestAction,TestCheck):
    """
    Provides the executing ability of each command-line in TestCase
    """
    def __init__(self, options=None):
        self.logger = Logger.getLogger()
        self.option = options

    def mixIn(self,pyClass,mixInClass):
        if mixInClass not in pyClass.__bases__:
            pyClass.__bases__ = (mixInClass,) + pyClass.__bases__

    def run(self,test,outputResult):
        self.logger.debug('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>init device<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        device = DeviceManager.getInstance().getDevice()

        case_name = '%s.%s' %(type( test).__name__,  test._testMethodName)
        expectResultPath = os.path.join(outputResult.dirs['ws_right'],case_name)
        expectResult = ExpectResult(expectResultPath)
        checker = Checker(self.option,device,outputResult,expectResult)
        self.mixIn(unittest.TestCase,testWorker)
        if isinstance(test,unittest.TestCase):
            test.setDeviceImpl(device)
            test.setChecker(checker)
            test(outputResult)

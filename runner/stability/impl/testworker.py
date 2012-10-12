#!/usr/bin/env python
import time, sys, os, shutil, datetime, string
from stability.util.log import Logger
from devicemanager import DeviceManager
from assertion import assertion
from store import store
import unittest
from imglib import imglib

class TestAction:

    def setDeviceImpl(self,deviceImpl):
        self.impl = deviceImpl

    def launch(self, component=None, flags=None):
        self.impl.startActivity(component,flags)
        return self
    
    def press(self,keyseq):
        self.impl.pressKey(keyseq)
        return self

    def touch(self,x,y):
        self.impl.touch(x,y)
        return self

    def input(self,content):
        self.impl.typeWord(content)
        return self

    def drag(self,start,end,time,steps):
        self.impl.drag(start,end,time,steps)
        return self

    def sleep(self,sec):
        self.impl.sleep(sec)
        return self

    def adbCmd(self,command):
        self.impl.adbcommand(command)
        return self

class TestCheck:

    def setChecker(self,checker):
        self.checkpoint = -1
        self.checker = checker

    def waitForScreen(self,name=None, timeout=10, rect=(0, 0, 1, 1), th=0.7):
        self.checker.waitForScreen(name,timeout,rect,th)
        return self

    def waitForString(self):
        return self
    
    def check(self):
        self.checker.check()
        return self

    def _compare(self,f1,f2):
        return self

    def _contain(self,full,sub):
        return self

class Checker(object):

    def __init__(self,options=None,deviceImpl=None,outputResult=None,expResult=None):
        self.logger = Logger.getLogger()
        self.option = options
        self.device = deviceImpl
        self.testResult = outputResult
        self.expectResult = expResult
        self._checkpoint = -1

    def check(self):
        if self.option['recording']:
            assert False,'dont support recording mode.'
        c = self.expectResult.getCurrentPath()
        self.logger.debug('check---check')
        self.logger.debug(c)
        path = self.testResult.dirs['all']
        self._checkpoint = self._checkpoint + 1
        names = self.basename(str(self._checkpoint)+'.wait')
        filename_snapshot = os.path.join(path, names['snapshot'])
        self.logger.debug('pathfull:'+filename_snapshot)
        
        r = self.device.takeSnapshot()
        r.writeToFile(filename_snapshot, 'png')
        assert os.path.exists(filename_snapshot),'%s file does not exists'% filename_snapshot
        assert os.path.exists(c),'%s file does not exists'% filename_snapshot
        imglib.assertExists(filename_snapshot,c)

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

        r = self.device.takeSnapshot()
        r.writeToFile(filename_snapshot, 'png') # snapshot
        #here ResultSender will upload snapshot to server by sid or tid
        #from handler import ResultSender
        #ResultSender.getInstance.addTask(path=filename_snapshot)
        #from pubsub import pub
        #pub.sendMessage('collectresult',path=filename_snapshot)
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
        #self.store = store()

    def mixIn(self,pyClass,mixInClass):
        if mixInClass not in pyClass.__bases__:
            pyClass.__bases__ = (mixInClass,) + pyClass.__bases__

    def run(self,test,result=None, expResult=None):
        self.outputResult = result
        self.expectResult = expResult
        device = DeviceManager.getInstance().getDevice()
        ####add check  
        checker = Checker(self.option,device,result,expResult)
        self.mixIn(unittest.TestCase,testWorker)
        if isinstance(test,unittest.TestCase):
            test.setDeviceImpl(device)
            test.setChecker(checker)
            test(self.outputResult)

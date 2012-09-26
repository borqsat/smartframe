#!/usr/bin/env python
import time, sys, os, shutil, datetime, string
from stability.util.log import Logger
from devicemanager import DeviceManager
from assertion import assertion
from store import store

class testWorker:
    """
    provides the executing ability of each command-line in TestCase
    """
    def __init__(self, options=None):
        self.logger = Logger.getLogger()
        self.option = options
        self.assertion = assertion()
        self.logger.debug('init store')
        self.store = store()
        self.device = DeviceManager.getInstance().getDevice()
        self._checkpoint = -1

    def run(self,test,result=None, eResult=None):
        self.itest = test
        self.testResult = result
        self.expResult = eResult
        self.itest.worker = self
        self.itest(self.testResult)

    def check(self):
        if self.option.recording:
            assert False,'dont support recording mode.'
        c = self.expResult.getCurrentPath()
        self.logger.debug('check-----------------------------------------------------------check')
        self.logger.debug(c)
        img = self.saveImage()
        return self


    def sleep(self,tsec):
        self.device.sleep(tsec)
        return self

    def startActivity(self, component=None, flags=None):
        self.device.startActivity(component, flags)
        return self

    def pressKey(self, keyseq):
        self.device.pressKey(keyseq)        
        return self

    def drag(self,start,end,time,steps):
        self.device.drag(start,end,time,steps)
        return self

    def touch(self,x,y):
        self.device.touch(x,y)
        return self

    def typeWord(self,content):
        self.device.typeWord(content)
        return self

    def screenSnapShot(self, filePath, ext):
        self.device.screenSnapShot(filePath, ext)
        return self

    def adbcommand(self, command):
        self.device.adbcommand(command)
        return self

    def _isValidName(self, name):
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

    # Save current screen snapshot, and subimage if rect is not None, and ocr
    # string if ocr is True
    def saveImage(self, name=None, rect=None, ocr=False):
        "Save the snapshot."
        if (name == None):
            self._checkpoint += 1
            name = str(self._checkpoint) + '.save'
        else:
            self.assertion.assertTrue(self._isValidName(name),'Invalid checkpoint name: %s.' % name)
            #if (not self._isValidName(name)):
            #    self.fail('Invalid checkpoint name: %s.' % name)
        self.logger.debug('Save snapshot at checkpoint: %s.' % name)
        
        #path = self.store.getWorkDir()
        if self.option.recording:
            path = self.testResult.dirs['right']
        elif self.option.testing:
            path = self.testResult.dirs['all']
        names = self.store.basename(name)
        #self.testResult.dirs['right'] = ''
        self.logger.debug('path:'+path)

        filename_snapshot = os.path.join(path, names['snapshot'])
        filename_checkpoint = os.path.join(path, names['checkpoint'])
        filename_ocr = os.path.join(path, names['ocr'])
        rect_screen = rect and self.device.convert_to_screen_rect(rect)
        
        r = self.device.takeSnapshot()
        r.writeToFile(filename_snapshot, 'png') # snapshot
        #here ResultSender will upload snapshot to server by sid or tid
        #from handler import ResultSender
        #ResultSender.getInstance.addTask(path=filename_snapshot)
        #####from pubsub import pub
        #####pub.sendMessage('collectresult',path=filename_snapshot)
        if rect_screen is not None: # save subimage (checkpoint)
            r.getSubImage(rect_screen).writeToFile(filename_checkpoint, 'png')
            if ocr:
                self.logger.debug('Save ocr file.')
                ocr_string = StringHelper.getString(filename_checkpoint)
                #save the OCR string to file
                f = file(filename_ocr, 'wb')
                try:
                    f.write(ocr_string)
                finally:
                    f.close()

    # Check if current screen contains string in @param expected.
    # If @param expected is None, then compare with recorded ocr file.
    #@param name: the name of the checkpoint, which is to identify the checkpoint.
    #@param expected: expected string or strings list. None means to compare
    #                 with recorded ocr result.
    #@param rect: rect of sub-image. NOTES: dont use the default value.
    #@return True if current screen contains strings in @param expected.
    def checkString(self, name=None, expected=None, rect=(0,0,1,1)):
        if (name == None):
            self._checkpoint += 1
            name = str(self._checkpoint) + '.check'
        else:
            self.assertion.assertTrue(self._isValidName(name),'Invalid checkpoint name: %s.' % name)
            #if (not self._isValidName(name)):
            #    self.fail('Invalid checkpoint name: %s.', name)
        
        self.saveImage(name=name, rect=rect, ocr=True)
        
        result = True
        names = self.store.basename(name)
        filename_right = os.path.join(self.store.getRightDir(), names['ocr'])
        filename = os.path.join(self.store.getWorkDir(), names['ocr'])

        if expected is None and not self._isRecording(): #we should compare two ocr files
            self.logger.debug('Checking string with recorded ocr file.')
            result = StringHelper.compareOcrFiles(filename_right, filename)
        elif expected is not None: # compare @param expected with OCR result.
            if type(expected) is type(''):
                stringlist = [expected]
            elif type(expected) is type([]):
                stringlist = expected
            else:
                self.fail('Error: Unknown type of expected!')
            if self._isRecording():
                filename = filename_right
            for s in stringlist:
                self.logger.debug('Checking string: %s', s)
                result &= StringHelper.checkContainStringInFile(s, filename)
        
        return result

    def waitForString(self, name, rect, expected, timeout):
        try:
            # Takes a screenshot
            self.logger.debug('Wait for screen String.' )
            if (name == None):
                self._checkpoint += 1
                name = str(self._checkpoint) + '.wait'
            else:
                self.assertion.assertTrue(self._isValidName(name),'Invalid checkpoint name: %s.' % name)
                #if (not self._isValidName(name)):
                #    self.fail('Invalid checkpoint name: %s.', name)
        
            if self._isRecording():
                #recording
                self.logger.debug('Wait for %d seconds and then save ocr string as standard one.', timeout)
                self.device.sleep(timeout)
                return self.checkString(name=name, expected=expected, rect=rect)
            else:
                # testing
                self.logger.debug('Waiting for string...')
                begin = time.time()
                while (time.time() - begin < timeout):
                    self.logger.debug('Elapsed %f seconds...', time.time() - begin)
                    self.device.sleep(1)
                    if self.checkString(name=name, expected=expected, rect=rect):
                        return True
                self.logger.debug('Timeout during waitForString.')
                return False
        except:
            self.logger.debug('Error during screen String!!!')  
        return self

    # Wait until current screen is almost same as standard one, or timeout
    # @param name: name of checkpoint, which is to identify the checkpoint.
    # @param timeout: timeout in secondes
    # @param rect: screen rectangle. (0,0,1,1) means the whole screen
    # @param th: threshold between 0 and 1 to check the difference.
    #            0 means the same picture; 1 means totally different.
    # @return false: timeout; true: current screen is almost same as standard one
    threshold = 0.9
    def waitForScreen(self, name=None, timeout=10, rect=(0, 0, 1, 1), th=threshold):
        self.logger.debug('Enter waitForScreen.')
        if (name == None):
            self._checkpoint += 1
            name = str(self._checkpoint) + '.wait'
        else:
            self.assertion.assertTrue(self._isValidName(name),'Invalid checkpoint name: %s.' % name)
            #if (not self._isValidName(name)):
            #    self.fail('Invalid checkpoint name: %s.', name)
        # recording?
        if self.option.recording:
            #recording
            self.logger.debug('Wait for %d seconds and then save snapshot as standard picture.'%timeout)
            self.device.sleep(timeout)
            #self.assertEqual(self.checkImage(name, rect), 0)
            assert self.checkImage(name, rect) == 0
            self.logger.debug('Waiting screen at checkpoint %s was saved.'%name)
            return True
        else:
            # testing
            self.logger.debug('Waiting for screen...')
            begin = time.time()
            while (time.time() - begin < timeout):
                self.logger.debug('Elapsed %f seconds...'% (time.time() - begin))
                self.device.sleep(1)
                diff = self.checkImage(name, rect)
                sys.stderr.write('diff rate :' + str(diff)+'\n')
                if (diff >= 0 and diff <= th):
                    self.logger.debug('Reach the waiting screen.')
                    #return True
                    self.assertion.assertTrue(True,'assert pass: Timeout during waitForScreen')
                    return
            self.logger.debug('Timeout during waitForScreen.')
            self.assertion.assertTrue(False,'assert fail: Timeout during waitForScreen')
        return self
    
    # Get the difference between current screen snapshot and previous one.
    # @return different rate. 0 means the same one; 1 means totally different.
    # @param name: name of checkpoint, which is to identify the checkpoint.
    # @param rect: screen rectangle. (0,0,1,1) means the whole screen
    def checkImage(self, name=None, rect=(0, 0, 1, 1)):
        """
        Check snapshot in specified rect and return the diff rate from standard one.
        (0,0,1,1) means the whole screen.
        """
        if (name == None):
            self._checkpoint += 1
            name = str(self._checkpoint) + '.check'
        else:
            self.assertion.assertTrue(self._isValidName(name),'Invalid checkpoint name: %s.' % name)
            #if (not self._isValidName(name)):
            #    self.fail('Invalid checkpoint name: %s.', name)
        
        ###self.assertFalse(rect is None) # rect should not be None as we must compare the checkpoint images.
        self.assertion.assertTrue(rect is not None)
        self.saveImage(name, rect)
        
        diff = 0
        if not self.option.recording: # not recording, so we should compare the image.
            self.logger.debug("Not recording, so it's a checkpoint.")
            names = self.store.basename(name)
            #import sys
            #sys.stderr.write(str(os.path.exists(os.path.join(self.workspace_result_right, names['checkpoint']))))
            filename_right = os.path.join(self.testResult.dirs['right'], names['checkpoint'])
            filename = os.path.join(self.testResult.dirs['all'], names['checkpoint'])
            #self.assertTrue(os.path.exists(filename_right) and os.path.exists(filename))
            self.assertion.assertTrue(os.path.exists(filename_right),'file does not exists %s '% filename_right)
            self.assertion.assertTrue(os.path.exists(filename),'file does not exists %s '% filename)
            # Compare the two images
            diff = self._compare(filename, filename_right)
            self.logger.debug("The diff at checkpoint %s is %f."%(name, diff))
        return diff

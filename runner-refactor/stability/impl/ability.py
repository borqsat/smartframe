#!/usr/bin/env python  
#coding: utf-8

'''
Module define the ability need to be inject to test case.
TODO:change image name
@version: 1.0
@author: borqsat
@see: null
'''
import os,time
from os.path import join
import recognization
from expectresult import ExpectResult

class Ability(object):
    '''
    Class to provide the assertion.
    '''
    def expect(self,name,interval=3,timeout=9,similarity=0.7,msg=None):
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
        @type similarity: float
        @param similarity: The minimum similarity a match should have. If omitted, the default is used
        @type msg:string
        @param msg: Output string if the expected image not found in the target image file. 
        @rtype: unittest.TestCase
        @return: a instance of unittest.TestCase which have the ability to interact with device and verify the checkpoint
        '''
        result = getattr(self, 'result')
        expect_result = ExpectResult(result.localpath['ws_testcase_right'])
        sub_path = expect_result.getCurrentCheckPointPath(name)
        full = expect_result.getFullCurrentCheckPointPath()
        dirs,filename = os.path.split(full)
        rect = filename.split('.')[1]
        names = '%s.%s.png' % (os.path.splitext(name)[0],rect)
        src_path = join(result.localpath['ws_testcase'], names)
        begin = time.time()
        while (time.time() - begin < timeout):
            success = self.takeSnapshot(path=src_path)
            if success and recognization.isRegionMatch(src_path,sub_path):
                return self
            time.sleep(interval)
        #setattr(self,'expect_result',expect_result)
        if not msg:
            reason = 'Fail Reason: Unable to find the expected image <%s> in current screen!' % os.path.basename(sub_path)
        else:
            reason = msg
        assert False, reason

    def exists(self,name,interval=None,timeout=None,similarity=0.7):
        '''
        Check whether the expected image was found that satisfy the minimum similarity requirement. If found return True, 
        If not found return False.
        @type name: string
        @param name: The expected image(png) file name.
        @type interval: int
        @param interval: The interval time after one check. Default value is 2 seconds.
        @type timeout: int
        @param timeout: The time of waitting the screen snapshot.default value is 4 seconds. See "runner/stability/sysconfig"
        @type similarity: float
        @param similarity: The minimum similarity a match should have. If omitted, the default is used
        @rtype: boolean
        @return: return ture if the expect check point exists in screen. false if not exists.
        '''
        #TODO add time out checking
        result = getattr(self, 'result')
        src = join(result.localpath['ws_testcase'], name)
        self.takeSnapshot(path=src)
        expect_result = ExpectResult(result.localpath['ws_testcase_right'])
        sub = expect_result.getCurrentCheckPointPath(name)
        is_exists = recognization.isRegionMatch(src,sub)
        return is_exists

    def find(self,text):
        '''-
        check text on screen.
        '''
        pass

    def find_log(self,tag):
        '''
        Check if the tag can be found from device log.
        '''
        pass
    
    def touch_image(self,name):
        #TODO add time out checking
        result = getattr(self, 'result')
        expect_result = ExpectResult(result.localpath['ws_testcase_right'])
        sub_path = expect_result.getCurrentCheckPointPath(name)
        full = expect_result.getFullCurrentCheckPointPath()
        dirs,filename = os.path.split(full)
        rect = filename.split('.')[1]
        names = '%s.%s.png' % (os.path.splitext(name)[0],rect)
        src_path = join(result.localpath['ws_testcase'], names)
        if self.takeSnapshot(path=src_path):
            point = recognization.getRegionCenterPoint(src=src_path,sub=sub_path)
        self.touch(x=point[0],y=point[1])
        return self
#!/usr/bin/env python
#coding: utf-8
''''' 
@author: b072
@license: None
@contact: hongbin.bao@borqs.com 
@see: http://ats.borqs.com/smartserver/
 
@version: 1.0
@todo[1.1]: a new story 

@note: SmartRunner Doc
@attention: None
@bug: None
@warning: None
'''

from org.sikuli.script import Finder
from org.sikuli.script import Pattern
import os,sys

def isRegionMatch(src,sub,similarity,msg=None):
    '''
    A method that allows to search a small image file from a large image file.

    @type src:string
    @param src:the path of large image file
    @type sub:string
    @param sub:the path of small image file
    @type similarity:float
    @param similarity:Value should between 0 and 1.0, The matching content in the region has a similarity 
    between 0 (not found) and 1 (found and it is per pixel exactly matches to the pattern). The value can be 
    advised, to search with a minimum similarity, so that some minor variations in shape and color can be 
    ignored. If nothing else is specified, Default searches with a minimum similarity of 0.7, which does what 
    is expected in general cases.
    @type msg:string
    @param msg:a custom argument.
    @return: True--If sub image can be found in src image. 
             False--If sub image can not be found in src image or exception was thrown.
    '''
    assert os.path.exists(src) , '%s %s' % ('No such file:',src)
    assert os.path.exists(sub) , '%s %s' % ('No such file:',sub)
    result = False
    recognizer = None
    try:
        recognizer = Finder(src)
        recognizer.find(sub,similarity)
        if recognizer.hasNext():
            result = True
        return result
    except Exception,e:
        print >> sys.stderr, str(e)
        return False
    finally:
        if recognizer != None:
            recognizer.destroy() # release the memory used by finder
        
def getRegionCenterPoint(src,sub,similarity,msg=None):
    '''
    A method that to obtain the center point coordinates of the matched region in the src image

    @type src:string
    @param src:the path of large image file
    @type sub:string
    @param sub:the path of small image file
    @type similarity:float
    @param similarity:Value should bwtween 0 and 1.0, The matching content in the region has a similarity between 0 (not found) and 1 (found and it is per pixel exactly matches to the pattern). The value can be advised, to search with a minimum similarity, so that some minor variations in shape and color can be ignored. If nothing else is specified, Default searches with a minimum similarity of 0.7, which does what is expected in general cases.
    @type msg:string
    @param msg:a custom argument.
    @return: (x-coordinate,y-coordinate)--the center point coordinates of the matched region in the src image
             None--If sub image can not be found in src image or exception was thrown.
    '''
    assert os.path.exists(src) , '%s %s' % ('No such file:',src)
    assert os.path.exists(sub) , '%s %s' % ('No such file:',sub)
    result = None
    recognizer = None
    try:
        recognizer = Finder(src)
        recognizer.find(sub,similarity)
        if recognizer.hasNext():
            region = recognizer.next()
            point = region.getCenter()
            result = (point.getX(),point.getY())
        return result
    except Exception,e:
        print >> sys.stderr, str(e)
        return ()
    finally:
        if recognizer != None:
            recognizer.destroy() # release the memory used by finder       

def getRegionTopleftPoint(src,sub,similarity,msg=None):
    '''
    A method that to obtain the left top point coordinates of the matched region in the src image

    @type src:string
    @param src:the path of large image file
    @type sub:string
    @param sub:the path of small image file
    @type similarity:float
    @param similarity:Value should bwtween 0 and 1.0, The matching content in the region has a similarity between 0 (not found) and 1 (found and it is per pixel exactly matches to the pattern). The value can be advised, to search with a minimum similarity, so that some minor variations in shape and color can be ignored. If nothing else is specified, Default searches with a minimum similarity of 0.7, which does what is expected in general cases.
    @type msg:string
    @param msg:a custom argument.  
    @return: (x-coordinate,y-coordinate)--the left top point coordinates of the matched region in the src image
             None--If sub image can not be found in src image or exception was thrown.
    '''
    assert os.path.exists(src) , '%s %s' % ('No such file:',src)
    assert os.path.exists(sub) , '%s %s' % ('No such file:',sub)
    result = None
    #recognizer = None
    try:
        recognizer = Finder(src)
        recognizer.find(sub,similarity)
        if recognizer.hasNext():
            region = recognizer.next()
            point = region.getTopLeft()
            result = (point.getX(),point.getY())
        return result
    except:
        return ()
    finally:
        if recognizer != None:
            recognizer.destroy() # release the memory used by finder


def getSimilarity(src,sub,similarity=0.7):
    result = None
    recognizer = None
    try:
        recognizer = Finder(src)
        recognizer.find(sub,similarity)
        if recognizer.hasNext():
            region = recognizer.next()
            score = region.getScore()
            print 'Match rate > 0.7'
            print 'Current match rate:'
            print score
        else:
            print 'Match rate < 0.7'
    finally:
        if recognizer != None:
            recognizer.destroy() # release the memory used by finder
#!/usr/bin/env python  
#coding: utf-8

'''
image compare lirbary
depend:
sudo apt-get install python-opencv
sudo apt-get install python-numpy
'''

import cv2
from cv2 import cv
import sys
import os

def isRegionMatch(src, sub, threshold=0.1):
    assert os.path.exists(src), 'file:<%s> not found!' % src
    assert os.path.exists(sub), 'file:<%s> not found!' % src
    for img in [src,sub]: assert os.path.exists(img) , "No such image:  %s" % (img)
    method = cv2.cv.CV_TM_SQDIFF_NORMED
    #Load the image
    sub = cv2.imread(sub)
    src = cv2.imread(src)
    #Check the image opened successful
    if not sub.data or not src.data:
        assert 'Open the image failed!!!'
    try:
        #Convert the image to gray
        sub_img = cv2.cvtColor(sub, cv2.CV_32FC1)
        src_img = cv2.cvtColor(src, cv2.CV_32FC1)
        #Try to match
        d = cv2.matchTemplate(sub_img,src_img, method)
        #Get the minimum squared difference
        minVal = cv2.minMaxLoc(d)[0]
        #Compared with the expected similarity
        if minVal < threshold:
            return True
        else: 
            return False
            
    except Exception,e:
        print >> sys.stderr, str(e)
        return False
    
def getRegionCenterPoint(src,sub,threshold):
    
    for img in [src,sub]: assert os.path.exists(img) , "No such image:  %s" % (img)
    method = cv2.cv.CV_TM_SQDIFF_NORMED
    #Load the image
    sub = cv2.imread(sub)
    src = cv2.imread(src)
    #Check the image opened successful
    if not sub.data or not src.data:
        assert "Open the image failed!!!"
    try:
        #Convert the image to gray
        sub_img = cv2.cvtColor(sub, cv2.CV_32FC1)
        src_img = cv2.cvtColor(src, cv2.CV_32FC1)
        #Try to match
        d = cv2.matchTemplate(sub_img,src_img, method)
        #Get the minimum squared difference
        minVal,_,minLoc,_ = cv2.minMaxLoc(d)
        #Get the let top (x,y) location
        minLoc_x_point,minLoc_y_point = minLoc
        #Compared with the expected similarity
        if minVal < threshold: 
            sub_img_row,sub_img_column = sub_img.shape[:2]
            center_point = (minLoc_x_point + int(sub_img_row/2),minLoc_y_point + int(sub_img_column/2))
            return center_point
        else:
            return None
            
    except Exception,e:
        print >> sys.stderr, str(e)
        return None
    
    
def getSubimageSimilarity(src,sub,threshold=0.2):
    for img in [src,sub]: assert os.path.exists(img) , "No such image:  %s" % (img)
    method = cv2.cv.CV_TM_SQDIFF_NORMED
    #Load the image
    sub = cv2.imread(sub)
    src = cv2.imread(src)
    #Check the image opened successful
    if not sub.data or not src.data:
        assert "Open the image failed!!!"
    try:
        #Convert the image to gray
        sub_img = cv2.cvtColor(sub, cv2.CV_32FC1)
        src_img = cv2.cvtColor(src, cv2.CV_32FC1)
        #Try to match
        d = cv2.matchTemplate(sub_img,src_img, method)
        #Get the minimum squared difference
        minVal = cv2.minMaxLoc(d)[0]
        #Compared with the expected similarity
#         if minVal < threshold: 
#             return minVal
#         else:
#             return None
        return minVal
    
    except Exception,e:
        print >> sys.stderr, str(e)
        return None


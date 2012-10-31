from org.sikuli.script import Finder
from org.sikuli.script import Pattern

def isRegionMatch(src,sub,similarity=0.7,msg=None):
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
    @return: True--If sub image can be found in src image . 
               False--If sub image can not be found in src image or exception was thrown.
    '''
    try:
        recognizer = Finder(src)
        recognizer.find(sub,similarity)
    except:
        return False
    if recognizer.hasNext():
        return True
    else:
        return False
        
def getRegionCenterPoint(src,sub,similarity=0.7,msg=None):
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
    try:
        recognizer = Finder(src)
        recognizer.find(sub,similarity)
    except:
        return None
    if recognizer.hasNext():
        region = recognizer.next()
        point = region.getCenter()
        return (point.getX(),point.getY())
    else:
        return None
    
def getRegionTopleftPoint(src,sub,similarity=0.7,msg=None):
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
    try:
        recognizer = Finder(src)
        recognizer.find(sub,similarity)
    except:
        return None
    if recognizer.hasNext():
        region = recognizer.next()
        point = region.getTopLeft()
        return (point.getX(),point.getY())
    else:
        return None

def assertExists(fullImgPath,subImgPath,msg=None):
    full = Finder(fullImgPath)
    sub = Pattern(subImgPath)
    full.find(sub)
    if full.hasNext():
        pass
    else:
        raise AssertionError

def isExists(fullImgPath,subImgPath,msg=None):
    full = Finder(fullImgPath)
    sub = Pattern(subImgPath)
    full.find(sub)
    if full.hasNext():
        return True
    else:
        return False

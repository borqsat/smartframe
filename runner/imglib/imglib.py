import sys
sys.path.append('/home/test/Desktop/runner/imglib/sikuli-script.jar')
from org.sikuli.script import Finder
from org.sikuli.script import Pattern
import os

def assertExists(fullImgPath,subImgPath,msg=None):
    #assert os.path.exists(fullImgPath),'%s%s'%(fullImgPath,' file does not exists!')
    #assert os.path.exists(subImgPath),'%s%s'%(subImgPath,' file does not exists!')
    full = Finder(fullImgPath)
    sub = Pattern(subImgPath)
    full.find(sub)
    if full.hasNext():
        pass
    else:
        raise AssertionError
        #assert False,'%s%s'%(msg,'Img does not exists.')

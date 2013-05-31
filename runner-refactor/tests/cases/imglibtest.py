#!/usr/bin/env python
import unittest,os
from libs.imglib import imglib
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SMALL_PATH = os.path.join('%s%s%s%s%s%s%s' % (WORKSPACE,os.sep,'tests',os.sep,'cases',os.sep,'small.png'))
LARGE_PATH = os.path.join('%s%s%s%s%s%s%s' % (WORKSPACE,os.sep,'tests',os.sep,'cases',os.sep,'large.png'))
COMPARE_PATH = os.path.join('%s%s%s%s%s%s%s' % (WORKSPACE,os.sep,'tests',os.sep,'cases',os.sep,'compare.png'))
CENTER_POINT_COORD = (74,362)
LEFTTOP_POINT_COORD = (46,332)
class ImagelibTest(unittest.TestCase):
    '''
    Unit test for imglib.
    monkeyrunner ut.py
    runner.ut.py
    '''

    def setUp(self):
        self.small = SMALL_PATH
        self.large = LARGE_PATH
        self.compare = COMPARE_PATH
    
    def testIsRegionMatch(self):
        self.assertTrue(imglib.isRegionMatch(self.large,self.small,similarity=0.7))
        self.assertTrue(imglib.isRegionMatch(self.large,self.small,similarity=0.9))
        self.assertTrue(imglib.isRegionMatch(self.large,self.small,similarity=1.0))
        self.assertFalse(imglib.isRegionMatch(self.large,self.compare,similarity=0.7))
        self.assertFalse(imglib.isRegionMatch(self.large,self.compare,similarity=0.9))
        self.assertFalse(imglib.isRegionMatch(self.large,self.compare,similarity=1.0))

    def testGetRegionCenterPoint(self):
        self.assertTrue(CENTER_POINT_COORD == imglib.getRegionCenterPoint(self.large,self.small,similarity=0.7))
        self.assertTrue(CENTER_POINT_COORD == imglib.getRegionCenterPoint(self.large,self.small,similarity=0.9))
        self.assertTrue(CENTER_POINT_COORD == imglib.getRegionCenterPoint(self.large,self.small,similarity=1.0))
        self.assertFalse(imglib.getRegionCenterPoint(self.large,self.compare,similarity=0.7))
        self.assertFalse(imglib.getRegionCenterPoint(self.large,self.compare,similarity=0.9))
        self.assertFalse(imglib.getRegionCenterPoint(self.large,self.compare,similarity=1.0))

    def testGetRegionTopleftPoint(self):
        self.assertTrue(LEFTTOP_POINT_COORD == imglib.getRegionTopleftPoint(self.large,self.small,similarity=0.7))
        self.assertTrue(LEFTTOP_POINT_COORD == imglib.getRegionTopleftPoint(self.large,self.small,similarity=0.9))
        self.assertTrue(LEFTTOP_POINT_COORD == imglib.getRegionTopleftPoint(self.large,self.small,similarity=1.0))
        self.assertFalse(imglib.getRegionTopleftPoint(self.large,self.compare,similarity=0.7))
        self.assertFalse(imglib.getRegionTopleftPoint(self.large,self.compare,similarity=0.9))
        self.assertFalse(imglib.getRegionTopleftPoint(self.large,self.compare,similarity=1.0))
        

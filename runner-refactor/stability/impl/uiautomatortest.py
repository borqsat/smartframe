#!/usr/bin/env python
import unittest,os
import uiautomator_device
import time

class UiAutomatorTest(unittest.TestCase):
    '''
    Unit test for uiautomator_device.py.
    '''
    def setUp(self):
        self.device = uiautomator_device.Device()

    def testTouchPoint(self):
        commands.getoutput('adb shell am start -a android.intent.action.INSERT -d content://com.android.contacts -n com.android.contacts/.activities.ContactEditorActivity')
        time.sleep(2)
        self.device.touch(307, 106).input("abc").press('back')
        time.sleep(2)

if __name__ == "__main__":
    unittest.main()




        
        

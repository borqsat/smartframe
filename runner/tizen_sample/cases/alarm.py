#!/usr/bin/env python
import unittest

""" 
@author: Li Hui
@maintain: Li Hui
@contact: hui.li@borqs.com

@note: Stability test cases for Alarm
"""

class AlarmTest(unittest.TestCase):

    def setUp(self):
        super(AlarmTest,self).setUp()

    def testAlarmAddDelete(self):
        """
        Summary:testAlarmAddDelete: Add and Delete an alarm
        Steps:1.Open Alarm app
              2.Touch Add button
              3.Tocuh Save button
              4.Delete the alarm
              5.Touch Back to exit Alarm app
        """
        self.touch((126,362),waittime=2)
        #.expect('2_noalarm.png')\
        #.touch('3_add.png')\
        #.expect('4_create_screen.png')\
        #.touch('5_save.png')\
        #.expect('6_ok.png')\
        #.touch('7_menu.png')\
        #.touch('8_delete.png')\
        #.touch('9_selectall.png')\
        #.touch('10_deletereal.png')\
        #.expect('2_noalarm.png')
        
    def tearDown(self):
        #self.touch('back.png').press('shome')
        super(AlarmTest,self).tearDown()

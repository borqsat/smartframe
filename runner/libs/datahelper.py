#!/usr/bin/python
import sys
import os
import string
import re
import commands

#call stability assistant service
cmd = 'adb shell am startservice -a com.borqs.intent.stabilitytest -e type '

#adb shell am startservice -a com.borqs.intent.stabilitytest -e type clearup -e feature contacts

#adb shell am startservice -a com.borqs.intent.stabilitytest -e type clearup -e feature calllogs

#adb shell am startservice -a com.borqs.intent.stabilitytest -e type clearup -e feature bookmarks

#adb shell am startservice -a com.borqs.intent.stabilitytest -e type clearup -e feature events

#adb shell am startservice -a com.borqs.intent.stabilitytest -e type clearup -e feature messages

class DataHelper:
    """
    The class is am to clearup application's data and generate test data during test.
    """
    def __init__(self):
        pass

    def clearup(self,appname):
        """
        Clear data from releated application's database.
        @device monkey device.
        @appname contacts,calllogs,bookmarks,events,messages
        """
        cmds = '%sclearup -e feature %s' % (cmd, appname) 
        commands.getoutput(cmds)

    #Contact
    def insertContact(self, contactname, contactnumber, count):
        """
        Insert a contat with phone number to DataBase.
        @device monkey device
        @contactname the contact's display name
        @contactnumber the contact's phone number.
        """
        #adb shell am startservice -a com.borqs.intent.stabilitytest -e type create -e feature contacts -e contactname Test -e contactnumber 100861 --ei contactcount 10
        cmds = '%screate -e feature contacts -e contactname %s -e contactnumber %s --ei contactcount %s' % (cmd, contactname, contactnumber, count) 
        commands.getoutput(cmds)

    #Call log
    def insertCallLog(self, calltype, callnumber):   
        """
        Insert a call log with the phone number and the type of the call
        @device monkey device.
        @calltype type of the call (incoming, outgoing or missed).
        @contactnumber The phone number as the user entered it.
        """ 
        #adb shell am startservice -a com.borqs.intent.stabilitytest -e type create -e feature calllogs -e calllogtype incoming -e calllognumber 100861
        cmds = '%screate -e feature calllogs -e calllogtype %s -e calllognumber %s' % (cmd, calltype, callnumber)
        commands.getoutput(cmds)

    #Bookmark
    def insertBrowserBookMark(self, title, url):
        """
        Insert a book mark for browser.
        @device monkey device.
        @title The user visible title of the bookmark item.
        @url The URL of the bookmark item.
        """ 
        #adb shell am startservice -a com.borqs.intent.stabilitytest -e type create -e feature bookmarks -e bookmarktitle att -e bookmarkurl www.att.com
        cmds = '%screate -e feature bookmarks -e bookmarktitle %s -e bookmarkurl %s' % (cmd, title, url)
        commands.getoutput(cmds)

    #Calendar event
    def insertCalendarEvent(self, title):
        """
        Insert a event for calendar.
        @device monkey device.
        @title The user visible title of the calendar events.
        """ 
        #adb shell am startservice -a com.borqs.intent.stabilitytest -e type create -e feature events -e eventtitle test
        cmds = '%screate -e feature events -e eventtitle %s' % (cmd, title)
        commands.getoutput(cmds)

    #Sms
    def insertReceivedSms(self, messagenumber, messagebody):
        """
        Insert a received sms.
        @device monkey device.
        @messagenumber phone number of the sender.
        @messagebody sms body of the received sms.
        """ 
        #adb shell am startservice -a com.borqs.intent.stabilitytest -e type create -e feature messages -e messagetype sms -e messagenumber 10086 -e messagebody test
        cmds = '%screate -e feature messages -e messagetype sms -e messagenumber %s -e messagebody %s' % (cmd, messagenumber, messagebody)
        commands.getoutput(cmds)

    #Mms
    def insertReceivedMms(self, messagenumber, messagebody, attachurl):
        """
        Insert a received mms.
        @device monkey device.
        @messagenumber phone number of the sender.
        @messagebody mms body of the received mms.
        @attachurl the url for attachment (/mnt/sdcard/Music/test.mp3)
        """ 
        #adb shell am startservice -a com.borqs.intent.stabilitytest -e type create -e feature messages -e messagetype mms -e messagenumber 10086 -e messagebody test -e messageurl /sdcard/Music/test.mp3
        cmds = '%screate -e feature messages -e messagetype mms -e messagenumber %s -e messagebody %s -e messageurl %s' % (cmd, messagenumber, messagebody, attachurl)
        commands.getoutput(cmds)

   

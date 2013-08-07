#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Internal APIs to implement sending invitation/verification email.
'''

import smtplib
from email.MIMEText import MIMEText

def __sendMail(receiver,subject,message):
    sender = 'borqsat@borqs.com'
    mailuser = 'borqsat@borqs.com'
    mailpass = '!QAZ2wsx3edc'

    msg = MIMEText(message,_subtype='plain',_charset='gb2312')      
    msg['Subject'] = subject      
    msg['From'] = sender     
    msg['To'] = ';'.join(receiver) 
    smtp = None
    try:
        smtp = smtplib.SMTP_SSL()
        smtp.connect('smtp.bizmail.yahoo.com')
        smtp.login(mailuser, mailpass)
        smtp.sendmail(sender, receiver, msg.as_string())
    except Exception, e:
        print e
    smtp.quit()

def sendVerifyMail(receiver, user, token):
    subject = 'Please active your email on SmartAT'

    msg = 'Hi,%s,\r\n\r\n' % (user)
    msg = msg + 'This mail sent out by smartAT, do not reply to it directly.\r\n'
    msg = msg + 'Your account \"%s\" has been created alreday.\r\n' % (user)
    msg = msg + 'Please verify your email via the url as below.\r\n'
    msg = msg + 'http://ats.borqs.com/smartserver/verify.html?token=%s\r\n' % (token)
    msg = msg + '\r\n\r\n'
    msg = msg + 'Best Regards\r\n'
    msg = msg + 'SmartAT Team\r\n'

    __sendMail(receiver,subject,msg)

def sendInviteMail(receiver, user, group, token):
    subject = 'Welcome to signup on SmartAT'

    msg = 'Hi,%s,\r\n\r\n' % (user)
    msg = msg + 'This mail sent out by smartAT, do not reply to it directly.\r\n'
    msg = msg + 'Your friend \"%s\" invite you to join group [%s].\r\n' % (user, group)
    msg = msg + 'You are welcome to signup your own account via the url below.\r\n'
    msg = msg + 'http://ats.borqs.com/smartserver/login.html?token=%s\r\n' % (token)
    msg = msg + '\r\n\r\n'
    msg = msg + 'Best Regards\r\n'
    msg = msg + 'SmartAT Team\r\n'

    __sendMail(receiver,subject,msg)

def sendErrorMail(context):
    subject='Case Error'

    msg = 'Hi,\r\n\r\n'
    msg = msg + 'This mail sent out by smartAT, do not reply to it directly.\r\n'
    msg = msg + 'Devices '+context['deviceid']+' happen error at '+ context['info']['issuetime']+  '.\r\n' 
    msg = msg + 'Error case name is '+context['info']['testcasename'] +' .\r\n'
    msg = msg + 'This session starts time is '+context['info']['starttime'] +' .\r\n'
    msg = msg + 'please go to http://ats.borqs.com/smartserver/ to checked it, Thanks!\r\n' 
    msg = msg + '\r\n\r\n'
    msg = msg + 'Best Regards\r\n'
    msg = msg + 'SmartAT Team\r\n'

    __sendMail(context['receiver'],subject,msg)


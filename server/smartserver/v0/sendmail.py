#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Internal APIs to implement sending invitation/verification email.
'''

import smtplib

__all__ = ['sendVerifyMail', 'sendInviteMail']


def __sendVerifyMail(receiver, user, token):
    sender = 'borqsat@borqs.com'
    subject = 'Please active your email on SmartAT'
    mailuser = 'borqsat@borqs.com'
    mailpass = '!QAZ2wsx3edc'

    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, receiver, subject))
    msg = msg + 'Hi,%s,\r\n\r\n' % (user)
    msg = msg + 'This mail sent out by smartAT, do not reply to it directly.\r\n'
    msg = msg + 'Your account \"%s\" has been created alreday.\r\n' % (user)
    msg = msg + 'Please verify your email via the url as below.\r\n'
    msg = msg + 'http://ats.borqs.com/smartserver/verify.html?token=%s\r\n' % (token)
    msg = msg + '\r\n\r\n'
    msg = msg + 'Best Regards\r\n'
    msg = msg + 'SmartAT Team\r\n'

    smtp = None
    try:
        smtp = smtplib.SMTP_SSL()
        smtp.connect('smtp.bizmail.yahoo.com')
        smtp.login(mailuser, mailpass)
        smtp.sendmail(sender, receiver, msg)
    except Exception, e:
        print e
    smtp.quit()


def __sendInviteMail(receiver, user, group, token):
    sender = 'borqsat@borqs.com'
    subject = 'Welcome to signup on SmartAT'
    mailuser = 'borqsat@borqs.com'
    mailpass = '!QAZ2wsx3edc'

    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, receiver, subject))
    msg = msg + 'Hi,%s,\r\n\r\n' % (user)
    msg = msg + 'This mail sent out by smartAT, do not reply to it directly.\r\n'
    msg = msg + 'Your friend \"%s\" invite you to join group [%s].\r\n' % (user, group)
    msg = msg + 'You are welcome to signup your own account via the url below.\r\n'
    msg = msg + 'http://ats.borqs.com/smartserver/login.html?token=%s\r\n' % (token)
    msg = msg + '\r\n\r\n'
    msg = msg + 'Best Regards\r\n'
    msg = msg + 'SmartAT Team\r\n'

    smtp = None
    try:
        smtp = smtplib.SMTP_SSL()
        smtp.connect('smtp.bizmail.yahoo.com')
        smtp.login(mailuser, mailpass)
        smtp.sendmail(sender, receiver, msg)
    except Exception, e:
        print e
    smtp.quit()


sendVerifyMail = __sendVerifyMail
sendInviteMail = __sendInviteMail

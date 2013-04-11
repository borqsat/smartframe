#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Internal APIs to implement sending invitation/verification email.
'''

import smtplib

__all__ = ['sendVerifyMail', 'sendInviteMail']


def __sendVerifyMail(receiver, user, token):
    sender = 'borqsat@borqs.com'
    subject = 'Please active your account from SmartAT'
    mailuser = 'borqsat@borqs.com'
    mailpass = '!QAZ2wsx3edc'

    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, receiver, subject))
    msg = msg + 'Hi:\r\n'
    msg = msg + '\r\nThis mail send from smartServer automatically, do not reply this mail directly.\r\n'
    msg = msg + '\r\nYour account \"%s\" has been initialized.\r\n' % (user)
    msg = msg + '\r\nPlease verify your current email via the url as below.\r\n'
    msg = msg + '\r\nsmart Server: http://ats.borqs.com/smartserver/verify.html?token=%s\r\n' % (token)
    msg = msg + '\r\nBest Regards!\r\n'
    msg = msg + 'smartServer Admin\r\n'

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
    subject = 'Please active your account from SmartAT'
    mailuser = 'borqsat@borqs.com'
    mailpass = '!QAZ2wsx3edc'

    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, receiver, subject))
    msg = msg + 'Hi:\r\n'
    msg = msg + '\r\nThis mail send from smartServer automatically, do not reply this mail directly.\r\n'
    msg = msg + '\r\nYour friend \"%s\" invite you to join group [%s].\r\n' % (user, group)
    msg = msg + '\r\nYou are welcome to signup your own account via the url below.\r\n'
    msg = msg + '\r\nsmart Server: http://ats.borqs.com/smartserver/login.html?token=%s\r\n' % (token)
    msg = msg + '\r\nBest Regards!\r\n'
    msg = msg + 'smartServer Admin\r\n'

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

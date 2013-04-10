#!/usr/bin/env python  
#coding: utf-8
'''
Module provides the ability to subscribe the topic used by smart runner.
@version: 1.0
@author: borqsat
@see: null
'''

from libs.pubsub import pub
from builder import TestBuilder
from resulthandler import ResultHandler

def collectResult(func):
    '''
    Decorator of function. It publishes messages to some topic
    '''
    def wrap(*args, **argkw):
        func(*args, **argkw)
        if True:
            content = (func.__name__,args)
            pub.sendMessage('collectresult',info=content)
        return func
    return wrap

def subscribe(topic):
    '''
    Public method to add topic and handler.The handler need to be implemented.
    @type topic: string
    @param topic: the name of topic need to be sucscribed.
    '''
    handler = ResultHandler()
    pub.subscribe(handler.handle,topic)
subscribe('collectresult')


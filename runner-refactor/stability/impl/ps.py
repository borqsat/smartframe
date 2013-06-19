#!/usr/bin/env python  
#coding: utf-8

'''
Module provides the ability to use pubsub.
@version: 1.0
@author: borqsat
@see: null
'''

from testuploader import RequestUtils
from libs.pubsub import pub
from devicemanager import DeviceManager
from log import logger

def emit(topic, *args, **kwargs):
    '''
    Function to send message to topic
    '''
    pub.sendMessage(topic,*args, **kwargs)

def on(topic, func):
    '''
    Function to subscribe topic and handler
    '''
    pub.subscribe(func, topic)
    logger.debug('subscribe topic:\'%s\' to method:\'%s\'' % (topic,func.__name__))


class Topics(object):
    '''
    Class for representing all topics used in smart runner.
    '''
    UPLOAD = 'upload'
    TOPIC_SESSION = 'session.status'
    TOPIC_SNAPSHOT = 'snapshot'
    TOPIC_MEMTRACK = 'memtrack'

class TopicsHandler(object):
    '''
    Class for handle the topic resuqest.
    '''
    @staticmethod
    def onUpload(data):
        '''
        Handle the message from upload chanel.
        @type data: {}
        @param data: a dictionary contains the result path
        '''
        #TestUploader.upload()
        pass

    @staticmethod
    def onSnapshot(data):
        '''
        Handle the data from snapshot chanel.
        @type data: binary
        @param data: a binary file of snapshot
        '''
        pass







#!/usr/bin/env python  
#coding: utf-8

'''
Module provides the ability to use pubsub.
@version: 1.0
@author: borqsat
@see: null
'''

from serialize import serializer
from testuploader import RequestUtils
from libs.pubsub import pub
from devicemanager import DeviceManager
from log import logger

def emit(topic, *args, **kwargs):
    '''
    Function to send message to topic
    '''
    pub.sendMessage(topic, *args, **kwargs)

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
    TOPIC_DEVICE = 'device.error'
    TOPIC_SESSION = 'session.status'
    TOPIC_RESULT = 'collectresult'
    TOPIC_SNAPSHOT = 'snapshot'
    TOPIC_MEMTRACK = 'memtrack'
    #TOPIC_SESSION = 'sessionstatus'
    #TOPIC_RESULT = 'collectresult'

class Message(object):
    """
    A simple container object for the components of a message: the 
    topic and the user data. Each listener called by sendMessage(topic, data)
    gets an instance of Message. The given 'data' is accessed
    via Message.data, while the topic name is available in Message.topic::
    
        def listener(msg):
            print "data is ", msg.data
            print "topic name is ", msg.topic
            print msg
            
    The example shows how a message can be converted to string.
    """
    def __init__(self, topic, data):
        self.topic = topic
        self.data  = data

    def __call__(self):
        emit(self.topic,self)

    def __str__(self):
        return '[Topic: '+ self.topic +',  Data: '+ self.data +']'

class TopicsHandler(object):
    '''
    Class for handle the topic resuqest.
    '''
    @staticmethod
    def onTopicResult(message):
        '''
        Handle the message from TOPIC_RESULT chanel. Persist data to local file.
        @type message: Message
        @param message: an instance of Message representing a test result
                        data {result: TCresult,name: TCname,time=TCtime}
        '''
        if message.topic == Topics.TOPIC_RESULT:
            serializer.serialize(data=message.data)
        else:
            raise Exception('handler exception')

    @staticmethod
    def onSnapshot(message):
        '''
        Handle the message from TOPIC_SNAPSHOT chanel.
        @type message: Message
        @param message: an instance of Message representing a snapshot
        '''
        #global SNAPSHOT_QUEUE
        if message.topic == Topics.SNAPSHOT:
            url = ''
            RequestUtils.send(method='POST',retry_count=3,url=url,data={'data':open(message.data)})
        else:
            raise Exception('handler exception')

    @staticmethod
    def onDeviceError(message):
        '''
        Handle the message from TOPIC_DEVICE chanel.
        @type message: Message
        @param message: an instance of Message representing a device error
        '''
        #global SNAPSHOT_QUEUE
        if message.topic == Topics.TOPIC_DEVICE:
            DeviceManager.getInstance().reset()
        else:
            raise Exception('handler exception')






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
import variables
import ConfigParser
import sys
from testuploader import ResultUploader
import hashlib
import json
import urllib2
import base64
import uuid
import os
import uuid
import variables

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
    AUTH = 'auth'
    UPLOAD = 'upload'
    SESSION = 'session'
    TOPIC_SESSION = 'session.status'
    TOPIC_SNAPSHOT = 'snapshot'
    TOPIC_MEMTRACK = 'memtrack'

class TopicsHandler(object):
    '''
    Class for handle the topic resuqest.
    '''
    @staticmethod
    def onAuth(data):
        '''
        Handle the data from snapshot chanel.
        @type data: binary
        @param data: a binary file of snapshot
        '''
        auth_url = None
        token = None
        account_name = data['account']
        password = data['password']
        #validate token if validation failed. get a new token.
        #TODO: add function to verify the token from server
        if os.path.exists(variables.TOKEN_CONFIG_PATH):
            return
        #read server config 
        server_info = ConfigParser.ConfigParser()
        server_info.read(variables.SERVER_CONFIG_PATH)
        auth_url = None
        try:
            auth_url = server_info.get('server','authentication_url')
            if not auth_url:
                raise
        except Exception,e:
            print 'invalid config file %s\n' % variables.SERVER_CONFIG_PATH
            #abort due to read error. sys.exit(1)

        #do auth
        md = hashlib.md5()
        md.update(base64.b64decode(password))
        pwd_encode = md.hexdigest()
        postdata = {'appid':'01','username':account_name,'password':pwd_encode}
        response = None
        try:
            request = urllib2.Request(auth_url)
            request.add_header('Content-Type','application/json')
            request.add_header('Accept', 'application/json')
            request.add_data(json.dumps(postdata))
            request.get_method = lambda: 'POST'
            response = urllib2.urlopen(request,timeout=10)
            json_feedback = response.read()
            dic = eval(json_feedback)
            if 'errors' in dic.keys():
                raise Exception('account name or password incorrect')
            token = dic['results']['token']
        except urllib2.URLError, ue:
            print ue
            sys.exit(1)
            
        except urllib2.HTTPError, he:
            print he
            sys.exit(1)

        except Exception, e:
            if hasattr(e, 'reason'):
                print 'Failed to reach a server.'
                print '%s %s' % ('Reason:',str(e.reason))
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print '%s %s' % ('Error code:',str(e.code))
            else:
                print '%s %s' % ('Get token failed:',str(e))
            sys.exit(1)      
        finally:
            if response != None:
                response.close()

        cf = ConfigParser.ConfigParser()
        cf.read(variables.TOKEN_CONFIG_PATH)
        if not cf.has_section('account'):
            cf.add_section('account')
        cf.set('account','account',account_name)
        cf.set('account','password',password)
        cf.set('account','token',token)
        with open(variables.TOKEN_CONFIG_PATH,'wb') as f:
            cf.write(f)
        #TODO: only save the token to .token file.
        
    @staticmethod
    def onUpload(data):
        '''
        Handle the message from upload chanel.
        @type data: {}
        @param data: a dictionary contains the result path
        '''
        ResultUploader.getInstance().upload(data['directory'])

    @staticmethod
    def onSnapshot(data):
        '''
        Handle the data from snapshot chanel.
        @type data: binary
        @param data: a binary file of snapshot
        '''
        pass





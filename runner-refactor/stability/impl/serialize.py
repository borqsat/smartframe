#!/usr/bin/env python  
#coding: utf-8

'''
Module provides the ability to serialize information 
@version: 1.1
@author: borqsat
@see: null
'''

class serializer(object):
    '''
    Class for serializing message.
    '''
    def __init__(self,file_path=None):
        pass

    def serialize(self,file_path, data):
        '''
        function to serialize info
        @type path: string
        @params path: abs path of the serial file path
        @type data: dictionary
        @params data: a dictionary contains the data content need to be sent
        @rtype: boolean
        @return: true if serialize sucess, false if fail
        '''
        #_serializeWithPickle(data,path,protocol=True)
        pass

    def unserialize(self):
        '''
        function to serialize info
        @type data: Messasge
        @params data: instance of Message
        @rtype: 
        @return: true if serialize sucess, false if fail
        '''
        #pkl_file = None
        #__serializeWithPickle(data,pkl_file,protocol=True)
        pass
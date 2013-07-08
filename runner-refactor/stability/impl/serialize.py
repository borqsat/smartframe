#!/usr/bin/env python  
#coding: utf-8

'''
Module provides the ability to serialize information 
@version: 1.0
@author: borqsat
@see: null
'''
import cPickle as pickle

class Serializer(object):
    '''
    Class for serializing message.
    '''

    @staticmethod
    def serialize(file_path, data):
        '''
        function to serialize info
        @type file_path: string
        @params file_path: abs path of the serial file path
        @type data: dictionary
        @params data: a dictionary contains the data content need to be persisted.
        '''
        with open(file_path, 'wrb') as f:
            pickle.dump(data, f)

    @staticmethod
    def unserialize(file_path):
        '''
        function to read the serialize info
        @type file_path: string
        @params file_path: abs path of the serial file path
        @rtype: {}
        @return: the serial data
        '''
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data
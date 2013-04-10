'''
Module define exceptions in smart runner.
@version: 1.0
@author: borqsat
@see: null
'''
import sys
class DeviceException(Exception):
        '''
        Class for representing device exceptions.
        '''
	def __init__(self,message):
		Exception.__init__(self,message)
		sys.stderr.write('%s ' % message)

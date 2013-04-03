import sys
class DeviceException(Exception):
	def __init__(self,message):
		Exception.__init__(self,message)
		sys.stderr.write('%s ' % message)
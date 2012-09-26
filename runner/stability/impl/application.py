import sys,time
from stability.util.log import Logger 
from builder import TestBuilder
from testrunner import *

class Application(object):
    def __init__(self,options=None):
        '''
        init looger,builder,and DeviceManager before testing start
        '''
        self.logger = Logger.getLogger()
        self.builder = TestBuilder.getBuilder(options)
        self.runner = TestRunner(options)

    def run(self):
        self.runner.runTest(self.builder.getTestSuites())
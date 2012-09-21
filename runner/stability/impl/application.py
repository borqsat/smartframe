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
        self.runner = TestRunner.getRunner(self.builder)

    def run(self):
        testsuites = self.builder.loadTestSuites()
        if self.builder.isRecording():
            self.logger.debug('test start -> recording') 
            self.runner.run(testsuites)
        if self.builder.isTesting():
            self.logger.debug('test start -> executing')
            for cycle in range(self.builder.getCycle()):
                self.logger.debug('start cycle:'+str(cycle))
                self.runner.run(testsuites)
                self.logger.debug('end cycle:'+str(cycle))
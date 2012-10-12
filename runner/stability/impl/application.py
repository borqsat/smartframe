import sys,time
from stability.util.log import Logger 
from builder import TestBuilder
from testrunner import TestRunner

class Application(object):
    def __init__(self,properties=None):
        '''
        init looger,builder,runner before testing start
        '''
        self.logger = Logger.getLogger()
        self.builder = TestBuilder.getBuilder(properties)
        self.runner = TestRunner(properties)

    def run(self):
        self.runner.runTest(self.builder.getTestSuites())

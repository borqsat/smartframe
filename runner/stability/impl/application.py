'''
Module provides the Application class, which launch a test session and register signal.
@version: 1.0
@author: borqsat
@see: null
'''

from builder import TestBuilder
from testrunner import TestRunner
from signal import signal, SIGINT,SIGTSTP
from resulthandler import stop

class Application(object):
    '''
    Application concept for represent a cycle of test.
    '''
    def __init__(self,properties):
        '''
        Init test builder test runner before testing start.
        @type properties: Obejct of CommandOptions
        @param properties: Instance of CommandOptions for user command line.
        '''
        signal(SIGINT, stop)
        signal(SIGTSTP, stop)
        self.builder = TestBuilder.getBuilder(properties)
        self.runner = TestRunner(properties)

    def run(self):
        '''
        Run the test suites.
        '''
        self.runner.runTest(self.builder.getTestSuites())

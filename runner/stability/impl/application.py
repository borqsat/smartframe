import sys,time,signal
from stability.util.log import Logger 
from builder import TestBuilder
from testrunner import TestRunner
from pubsub import pub

class Application(object):
    def __init__(self,properties=None):
        '''
        init looger,builder,runner before testing start
        '''
        self.logger = Logger.getLogger()
        self.builder = TestBuilder.getBuilder(properties)
        self.runner = TestRunner(properties)

    def run(self):
        #signal.signal(signal.SIGINT, signal_handler)
        self.runner.runTest(self.builder.getTestSuites())

def signal_handler(signal, frame):
        pub.sendMessage('collectresult',sessionStatus='sessionstop')
        sys.exit(0)
'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

from builder import TestBuilder
from testrunner import TestRunner

class Application(object):
    '''
    Application context.
    '''
    def __init__(self,properties):
        '''
        Init test builder test runner before testing start.

        @type properties: Obejct of CommandOptions
        @param properties: Instance of CommandOptions for user command line.
        '''
        self.builder = TestBuilder.getBuilder(properties)
        self.runner = TestRunner(properties)

    def run(self):
        '''
        Run the test suites.
        '''
        self.runner.runTest(self.builder.getTestSuites())
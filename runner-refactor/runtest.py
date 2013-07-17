import sys
from stability import logger,Options,TestBuilder,TestRunner,TestResultImpl,Authentication,on,Topics,TopicsHandler

def run_cmdline(arguments):
    '''
    Command line execution entry point for running tests.
    @type argv: []
    @params argv: input from command line
    '''
    logger.debug('start...')
    options = Options(arguments)

    if options['upload']:
        on(Topics.UPLOAD, TopicsHandler.onUpload)
        Authentication.auth()
    #if options['screenmonitor']: on(Topics.TOPIC_SNAPSHOT, TopicsHandler.onSnapshot)

    test_builder = TestBuilder(options)

    tests = test_builder.getTestSuite()

    test_result = TestResultImpl(options)

    runner = TestRunner(test_result)
    runner.run(tests)


if __name__ == '__main__':
    run_cmdline(sys.argv)

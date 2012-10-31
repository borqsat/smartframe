import sys,os,datetime,string,time,getopt
from stability import Application
#from urlgrabber3.urlgrabber.keepalive import HTTPHandler
class CommandOptions(object):
    def __init__(self,argv):
        timestamp = time.strftime('%Y.%m.%d-%H.%M.%S',time.localtime(time.time()))
        self.data = {'recording':False,
                     'testing':False,
                     'cycle':1,
                     'duration':None,
                     'plan':None,
                     'testcase':None,
                     'testcase':None,
                     'starttime':timestamp,
                     'uploadresult':False,
                     'screenmonitor':False,
                     'downloadsnapshot':False,
                     'random':False}
        self.parse(argv)

    def parse(self,argv):
        try:
            opts, args = getopt.getopt(argv[1:], 'hrtc', ['help','recording','testing','cycle=','plan=','testcase=','uploadresult','screenmonitor','random'])
        except getopt.GetoptError, err:
        # print help information and exit:
            #print str(err) # will print something like "option -a not recognized"
            self.showUsage()
            sys.exit(2)
        for opt, arg in opts:
            #print opt
            if opt in ('-h', '--help'):
                self.showUsage()
            elif opt in ('-r', '--recording'):
                self.data['recording'] = True
            elif opt in ('-t', '--testing'):
                self.data['testing'] = True
            elif opt in ('-c','--cycle'):
                self.data['cycle'] = arg
                #print arg
            elif opt in ('--random'):
                self.data['random'] = True
            elif opt in ('--plan'):
                self.data['plan'] = arg
                #print arg
            elif opt in ('--testcase'):
                self.data['testcase'] = arg
                #print arg
            elif opt in ('--uploadresult'):
                self.data['uploadresult'] = True
            elif opt in ('--screenmonitor'):
                self.data['screenmonitor'] = True

    def getProperties(self):
        return self.data
        #if self.data.has_key(name):
        #    value = self.data[name]
        ##else:
        #    raise 'miss data name'
        #return value

    def showUsage(self):
        print 'Usage:'
        print 'monkeyrunner starttest.py '
        print '                         [-t|--testing]'
        print '                         [--uploadresult]'
        print '                         [--uploadsnapshot]'
        print '                         [--downloadsnapshot]'
        print '                         [--random]'
        print '                         [--runner=html,xml,text]'
        print '                         [--cycle=number]'
        print '                         [--duration=format]'
        print '                         [--testcase=name ]'
        print '                         [--plan=file]]'
        print '-ur or --uploadresult: Enable or disbale uploadresult features. Upload test result of each testcase to the result server.'
        print '-sm or --screenmonitor: Enable or disbale screenmonitor features. Upload the screen snapshot to server non-stop' 
        print '-ds or --downloadsnapshot: Enable or disbale downloadsnapshot features. Download the right snapshot of each testcase from the snapshot server.'
        print '-ra or --random: Enable or disbale random features. Run test case sequence in the random order.'
        print '--runner=runnername   : Specify the test runner . Default is text runner.'
        print '-t or --testing  : Enable testing. Disable testing without the option.'
        print '--cycle=number   : The count of test cycles before ending the test. Default is 1.'
        print '--duration=format: The minumum test duration before ending the test. It has higher priority than --cycle option.'
        print '                   Here format must follow next format: xxDxxHxxMxxS.'
        print '                   e.g. --duration=1D09H30M12S, which means 1 day, 09 hours, 30 minutes and 12 seconds.'
        print '--testcase=name  : Specify the name of test case, following next format: module.testcase.method'
        print '--plan=file    : Specify the config file name. '
        print '                   You can specify tests list in "tests" section in the file.'
        print '                   e.g.'
        print '                       [tests]'
        print '                       module.testcase1.method1=10'
        print '                       module.testcase1.method2=5'
        print '                       module.testcase2.method1=12'


def main(**argkw):
    options = CommandOptions(sys.argv)
    Application(options.getProperties()).run()

if (__name__ == '__main__'):
    main()



import sys,os,datetime,string,time
from stability import Application

class CommandOptions(object):
    def __init__(self, argv):
        timestamp = time.strftime('%Y.%m.%d-%H.%M.%S',time.localtime(time.time()))
        self.data = {'recording':False,
                     'testing':False,
                     'cycle':1,
                     'duration':None,
                     'plan':None,
                     'testcase':None,
                     'starttime':timestamp,
                     'uploadresult':False,
                     'screenmonitor':False,
                     'downloadsnapshot':False,
                     'random':False}
        if len(argv) > 1:
            for arg in argv[1:]:
                if arg == '--recording' or arg == '-r':
                    self.data['recording'] = True
                elif arg == '--testing' or arg == '-t':
                    self.data['testing'] = True
                elif arg == '--uploadresult' or arg == '-ur':
                    self.data['uploadresult'] = True
                elif arg == '--screenmonitor' or arg == '-sm':
                    self.data['screenmonitor'] = True
                elif arg == '--downloadnapshot' or arg == '-ds':
                    self.data['downloadnapshot'] = True
                elif arg == '--random' or arg == '-ra':
                    self.data['random'] = True
                                                            
                elif string.find(arg, '--cycle=') == 0:
                    value = arg[len('--cycle='):]
                    self.data['cycle'] = int(value)
                elif string.find(arg, '--duration=') == 0:
                    value = arg[len('--duration='):]
                    value = string.lower(value)
                    begin=0
                    days = hours = minutes = seconds = 0
                    for i, v in enumerate(value):
                        if v == 'd':
                            days = int(value[begin:i])
                            begin = i + 1
                        elif v == 'h':
                            hours = int(value[begin:i])
                            begin = i + 1
                        elif v == 'm':
                            minutes = int(value[begin:i])
                            begin = i + 1
                        elif v == 's':
                            seconds = int(value[begin:i])
                            begin = i + 1
                    if begin == 0:
                        raise ValueError, 'Duration format error.'
                    self.data['duration'] = datetime.timedelta(days=days,
                                                               hours=hours,
                                                               minutes=minutes,
                                                               seconds=seconds)
                elif string.find(arg, '--plan=') == 0:
                    value = arg[len('--plan='):]
                    if self.data['plan'] is None:
                        self.data['plan'] = value
                    else:
                        raise ValueError, 'Invalid options...'
                elif string.find(arg, '--testcase=') == 0:
                    value = arg[len('--testcase='):]
                    if self.data['testcase'] is None:
                        self.data['testcase'] = value
                    else:
                        raise ValueError, 'Invalid options...'
                else:
                    raise ValueError, 'Invalid options...'
    
    def __getattribute__(self, name):
        try:
            v = object.__getattribute__(self, name)
        except AttributeError:
            d = self.data
            if d.has_key(name):
                v = d[name]
            else:
                raise
        return v
    
    @classmethod
    def showUsage(cls):
        print 'Usage:'
        print 'monkeyrunner starttest.py [-r|--recording]'
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
        print '-r or --recording: Enable recording before testing. Disable recording without the option.'
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
    Application(options).run()

if (__name__ == '__main__'):
    main()



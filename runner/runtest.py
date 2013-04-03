#!/usr/bin/env python  
#coding: utf-8  
''''' 
@author: b072
@license: None
@contact: hongbin.bao@borqs.com 
@see: http://ats.borqs.com/smartserver/
 
@version: 1.0 
@todo[1.1]: a new story 
 
@note: SmartRunner Doc
@attention: None 
@bug: None
@warning: None
'''  
__version__ = '1.0'
import sys,os,datetime,string,time,getopt
from stability import Application
class CommandOptions(object):
    def __init__(self,argv):
        timestamp = time.strftime('%Y.%m.%d-%H.%M.%S',time.localtime(time.time()))
        self.data = {'recording':False,
                     'testing':True,
                     'cycle':'1',
                     'plan':None,
                     'testcase':None,
                     'starttime':timestamp,
                     'uploadresult':False,
                     'user':None,
                     'password':None,
                     'screenmonitor':False,
                     'downloadsnapshot':False,
                     'random':False,
                     'product':None}
        self.parse(argv)

    def parse(self,argv):
        if len(argv)<2:
            print 'arguments missed.'
            self.showUsage()
            sys.exit(2)            
        try:
            opts, args = getopt.getopt(argv[1:], 'hrtc', ['help','recording','testing','cycle=','plan=','testcase=','uploadresult','user=','password=','screenmonitor','random','product='])
        except getopt.GetoptError, err:
            self.showUsage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.showUsage()
                sys.exit(2)
            elif opt in ('-r', '--recording'):
                self.data['recording'] = True
            elif opt in ('-t', '--testing'):
                self.data['testing'] = True
            elif opt in ('-c','--cycle'):
                self.data['cycle'] = arg
            elif opt in ('--random'):
                self.data['random'] = True
            elif opt in ('--plan'):
                self.data['plan'] = arg
            elif opt in ('--testcase'):
                self.data['testcase'] = arg
            elif opt in ('--product'):
                self.data['product'] = arg
            elif opt in ('--uploadresult'):
                self.data['uploadresult'] = True
            elif opt in ('--user'):
                self.data['user'] = arg
            elif opt in ('--password'):
                self.data['password'] = arg
            elif opt in ('--screenmonitor'):
                self.data['screenmonitor'] = True
        self.validateInput()

    def validateInput(self):
        if self.data['product'] is None:
            print 'error! please specify product name: --product productname'
            sys.exit(2)
        else: 
            if not os.path.exists(self.data['product']):
                print '%s "%s" %s' % ('error!',self.data['product'],'product folder does not exist.')
                sys.exit(2)

        if self.data['testcase'] is not None and self.data['plan'] is not None:
            print 'error! can''/t specify "--testcase" and "--plan"'
            sys.exit(2)

        #if self.data['uploadresult'] is True:
        #    if self.data['user'] is None or self.data['password'] is None:
        #        print 'error! \'user\' or \'password\' missed!'
        #        sys.exit(2)


    def getProperties(self):
        return self.data

    def showUsage(self):
        print 'Usage:'
        print 'monkeyrunner runtest.py --testcase moudlename.testClassName.testMethodName --product productname'
        print 'monkeyrunner runtest.py --plan productname/plan/planfilename --product productname --cycle 10 --uploadresult'
        print 'All supported arguments:'
        print 'monkeyrunner runtest.py '
        print '                         [--testcase casename]'
        print '                         [--plan planfile]'
        print '                         [--cycle number]'
        print '                         [--product productname]'
        print '                         [--uploadresult]'
        print '--testcase casename  : Specify the name of test case, following next format: module.testcase.testmethod'
        print '--cycle number   : The count of test cycles before ending the test. If you ignore this option. Default value is 1.'
        print '--product productname : The name of product test case which want to execute. You must specify this option in command line. '
        print '--uploadresult: Enable or disbale uploadresult features. Upload test result of each testcase to the result server.\
        If enable this option. Please make sure your computer\'s network available. If network unavailable. You may cant start the test\
        or lost test result data on server'
        print '--plan planfilepath    : Specify the test case plan file  relative or absolute path.'
        print '                   You can specify tests list in "tests" section in the file.'
        print '                   e.g.'
        print '                       [tests]'
        print '                       module.testcase1.method1=10'
        print '                       module.testcase1.method2=5'
        print '                       module.testcase2.method1=12'

def main(**argkw):
    '''
    Accept command line input.
    '''
    options = CommandOptions(sys.argv)
    Application(options.getProperties()).run()

if (__name__ == '__main__'):
    main()

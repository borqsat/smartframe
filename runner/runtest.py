#!/usr/bin/env python  
#coding: utf-8  
''''' 
@author: Arthur 
@license: None 
@contact: hongbin.bao@borqs.com 
@see: www.borqs.com
 
@version: 1.0 
@todo[1.1]: a new story 
 
@note: SmartRunner Doc
@attention: None 
@bug: None
@warning: None
'''  

import sys,os,datetime,string,time,getopt
from stability import Application
class CommandOptions(object):
    def __init__(self,argv):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.data = {'recording':False,
                     'testing':True,
                     'cycle':1,
                     'duration':None,
                     'plan':None,
                     'testcase':None,
                     'testcase':None,
                     'starttime':timestamp,
                     'uploadresult':False,
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
            opts, args = getopt.getopt(argv[1:], 'hrtc', ['help','recording','testing','cycle=','plan=','testcase=','uploadresult','screenmonitor','random','product='])
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
            elif opt in ('--screenmonitor'):
                self.data['screenmonitor'] = True

    def getProperties(self):
        return self.data

    def showUsage(self):
        print 'Usage:'
        print 'monkeyrunner runtest.py --testcase productname.cases.testClassName.testMethodName --product productname'
        print 'monkeyrunner runtest.py --plan productname/plan/planfilename --product productname --cycle 10 --uploadresult'
        print 'All supported arguments:'
        print 'monkeyrunner runtest.py '
        print '                         [--testcase casename]'
        print '                         [--plan planfile]'
        print '                         [--cycle number]'
        print '                         [--product productname]'
        print '                         [--uploadresult]'
        print '--testcase casename  : Specify the name of test case, following next format: module.testcase.method'
        print '--cycle number   : The count of test cycles before ending the test. Default is 1.'
        print '--product productname : The name of product test case which want to execute.'
        print '--uploadresult: Enable or disbale uploadresult features. Upload test result of each testcase to the result server.'
        print '--plan planfile    : Specify the test case plan file name. '
        print '                   You can specify tests list in "tests" section in the file.'
        print '                   e.g.'
        print '                       [tests]'
        print '                       product.module.testcase1.method1=10'
        print '                       product.module.testcase1.method2=5'
        print '                       product.module.testcase2.method1=12'


def main(**argkw):
    '''
    Accept command line input.
    '''
    options = CommandOptions(sys.argv)
    Application(options.getProperties()).run()

if (__name__ == '__main__'):
    main()

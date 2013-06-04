#!/usr/bin/env python  
#coding: utf-8

'''
Class for options.

'''

import sys,getopt,time,os,ConfigParser
from os.path import dirname,abspath,join

__version__ = '0.1'
WORK_SPACE = dirname(dirname(dirname(abspath(__file__))))
USER_CONFIG_FILE = join(WORK_SPACE,'user.config')
SYSTEM_CONFIG_FILE = join(WORK_SPACE,'system.config')

class BaseOptions(object):

    _client_options = {'workspace'     : WORK_SPACE,
                       'upload'        : False,
                       'screenmonitor' : False
    }

    def __init__(self):
        self._client_options = self._client_options.copy()
        if getattr(self,'_extra_client_options', None):
            self._client_options.update(self._extra_client_options)
    
    def __setitem__(self,name,value):
        if name not in self._client_options:
            raise KeyError('Non-existing \'%s\'' % name)
        self._client_options[name] = value

    def __getitem__(self,name):
        if name not in self._client_options:
            raise KeyError('Non-existing \'%s\'' % name)          
        return self._client_options[name]

    def update(self,t):
        self._client_options.update(t)

class Options(BaseOptions):
    '''
    Class for representing all options.
    '''
    _extra_client_options = {'platform'      : '',
                             'product'       : '',
                             'plan'          : '',
                             'cycle'         : 1,
                             'testcase'      : '',
                             'starttime'     : time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time())),
                             'random'        : False,
                             'user'          : '',
                             'password'      : ''
                            }

    def __init__(self,argv):
        super(Options,self).__init__()
        self._parseCmdlineOptions(argv)
        self._parseConfigOptions(SYSTEM_CONFIG_FILE)
        #if self['upload']: self._parseUserOptions(USER_CONFIG_FILE)

    def _parseCmdlineOptions(self,argv):
        if len(argv)<2:
            print 'arguments missed.'
            self._showUsage()
            sys.exit(2)
        try:
            opts, args = getopt.getopt(argv[1:], 'hc:', ['help','cycle=','user=','password=','plan=','testcase=','upload','screenmonitor','random','product=','platform='])
        except getopt.GetoptError, err:
            print 'parser cmdline error'
            self._showUsage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self._showUsage()
                sys.exit(2)
            elif opt in ('-c','--cycle'):
                self['cycle'] = arg
            elif opt in ('--random'):
                self['random'] = True
            elif opt in ('--plan'):
                self['plan'] = arg
            elif opt in ('--testcase'):
                self['testcase'] = arg
            elif opt in ('--product'):
                self['product'] = arg
            elif opt in ('--platform'):
                self['platform'] = arg
            elif opt in ('--upload'):
                self['upload'] = True
            elif opt in ('--screenmonitor'):
                self['screenmonitor'] = True
            elif opt in ('--user'):
                self['user'] = arg
            elif opt in ('--password'):
                self['password'] = arg
    
    def validation(self):
        pass

    def _showUsage(self):
        print '--------------------------------------------------'
        print '--------------------------------------------------'
        print '-------                 *             -----------'
        print '------- **   **    *        **   *   *-----------'
        print '-------*  *  * *  ***   *  *  *  * * *-----------'
        print '------- **   **    ***  *   **   *   *-----------'
        print '-------      *          *             -----------'
        print '-------      *          *             -----------'
        print '--------------------------------------------------'
        print '--------------------------------------------------'
        print 'python runtest.py --testcase moudlename.testClassName.testMethodName --product productname'
        print 'python runtest.py --plan productname/plan/planfilename --product productname --cycle 10 --upload --user xxx --password xxxx'
        print 'All supported arguments:'
        print 'python runtest.py '
        print '                         [--testcase casename]'
        print '                         [--plan planfile]'
        print '                         [--cycle number]'
        print '                         [--product productname]'
        print '                         [--upload]'
        print '                         [--user]'
        print '                         [--password]'
        print '                         [--screenmonitor]'
        print '--testcase casename      : Specify the name of test case, following next format: module.testcase.testmethod'
        print '--cycle number           : The count of test cycles before ending the test. If you ignore this option. Default value is 1.'
        print '--product productname    : The name of product test case which want to execute. You must specify this option in command line. '
        print '--upload                 : Enable or disbale uploadresult features. Upload test result of each testcase to the result server.\
If enable this option. Please make sure your computer\'s network available. If network unavailable. You may cant start the test\
or lost test result data on server'
        print '--user xxxxxxxxxxxxx     : if enable \'--upload\' need to validate the user account name of smartserver'
        print '--password xxxxxxxxx     : if enable \'--upload\' need to validate the user account password of smartserver'
        print '--screenmonitor          : enable or disable the screeen real-time function'
       
        print '--plan planfilepath      : Specify the test case plan file  relative or absolute path.'
        print '                           You can specify tests list in "tests" section in the file.'
        print '                           e.g.'
        print '                           [tests]'
        print '                           module.testcase1.method1=10'
        print '                           module.testcase1.method2=5'
        print '                           module.testcase2.method1=12'

    def _parseConfigOptions(self,config_file_path):
        config = ConfigParser.ConfigParser()
        config.optionxform = lambda x: x
        config.read(config_file_path)
        for section in config.sections():
            for item in config.items(section):
                #print (dict([item]))
                self.update(dict([item]))


##############test method
def test():
    op = BaseOptions()
    print op['reportdir']
    print op['workspace']

def test1():
    op = Options(sys.argv)
    print op['cycle']
    print op['starttime']
    print op['user']
    print op['password']
    print op['screenmonitor']
    print op['after_touch_time']
    print op['after_launch_time']
      

if __name__ == '__main__':
    #test()
    test1()

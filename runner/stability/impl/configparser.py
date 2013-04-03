'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import os,string,sys
import ConfigParser
from testconfig import Account,SystemConfig
class Parser(object):
    '''Class for reading the system config file.Like case plan file and sysconfig'''
    SYS_CONFIG_FILE = os.path.join('%s%s%s' % (os.path.dirname(os.path.dirname(__file__)),os.sep,'sysconfig'))
    PRODUCT_CONFIG_FILE = ''

    @staticmethod
    def getTestConfig(path):
        '''Get test case list from test plan file'''
        return readTestsFromConfigFile(path)

    @staticmethod
    def getDeviceLogConfig():
        '''Get the path of log output directory'''
        config = ConfigParser.ConfigParser()
        config.read(Parser.SYS_CONFIG_FILE)
        log = config.get('devicelog','log')
        return log

    @staticmethod
    def getSystemConfig():
        '''Get the idle time defination from sysconfig file'''
        sysConfig = SystemConfig()
        config = ConfigParser.ConfigParser()
        config.read(Parser.SYS_CONFIG_FILE)
        for item in config.items('time'):
            sysConfig.add(item)
        return sysConfig

    @staticmethod
    def getUserAccountConfig():
        '''Get the account info for SmartServer from sysconfig file'''
        account = Account()
        config = ConfigParser.ConfigParser()
        config.read(Parser.SYS_CONFIG_FILE)
        for item in config.items('user'):
            account.add(item)
        return account

    @staticmethod
    def setUserAccountConfig():
        '''Set the user account value for SmartServer'''
        account = Account()
        config = ConfigParser.ConfigParser()
        config.read(Parser.SYS_CONFIG_FILE)
        for item in config.items('user'):
            account.add(item)
        return account

def readTestsFromConfigFile(name):
    '''Get the test case sequence as a list of string from test paln file'''
    if not os.path.exists(name):
        print >>sys.stderr, 'Plan file does not exists.'
        sys.exit(1)
    # TODO: ConfigParser is better....
    # We don't use ConfigParser.ConfigParser here, because python2.6 didn't
    # support ordereddict... So we have to read it ourself.
    tests = []
    f = open(name)
    try:
        tests_section = False
        for l in f:
            if tests_section:
                if _isSection(l):
                    break
                else:
                    o = _getOption(l)
                    if o is not None:
                        try:
                            k = o[0]
                            v = int(o[1])
                            tests.append((k, v))
                        except Exception, e:
                            #print >>sys.stderr, str(e)
                            sys.exit(2)
            else:
                if _getSection(l) == 'tests':
                    tests_section = True
    except Exception, e:
        #print >>sys.stderr, str(e)
        sys.exit(2)
    finally:
        f.close()
    return tests

def _isSection(s):
    s = string.strip(s)
    if _isComment(s):
        return False
    return len(s) >= 3 and s[0] == '[' and s[-1:] == ']' and len(string.strip(s[1:-1])) > 0

def _getSection(s):
    s = string.strip(s)
    if _isSection(s):
        return string.strip(s[1:-1])
    else:
        return None

def _isOption(s):
    s = string.strip(s)
    if _isComment(s):
        return False
    ls = string.split(s, '=')
    return len(ls) == 2 and len(string.strip(ls[0])) > 0 and len(string.strip(ls[1])) > 0

def _isComment(s):
    s = string.strip(s)
    return len(s) > 0 and s[0] == '#'

def _getOption(s):
    if _isOption(s):
        ls = string.split(s, '=')
        return (string.strip(ls[0]), string.strip(ls[1]))
    else:
        return None

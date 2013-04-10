'''
Module provides the Parser class which used to parse the config file.
@version: 1.0
@author: borqsat
@see: null
'''

import os,string,sys
import ConfigParser
from testconfig import Account,SystemConfig
class Parser(object):
    '''
    Class for reading config file.
    '''
    SYS_CONFIG_FILE = os.path.join('%s%s%s' % (os.path.dirname(os.path.dirname(__file__)),os.sep,'sysconfig'))
    PRODUCT_CONFIG_FILE = ''

    @staticmethod
    def getTestConfig(path):
        '''
        Return test case list.
        @type path: string
        @param path: the path of test case plan file
        @rtype: list
        @return: a list of test case
        '''
        return readTestsFromConfigFile(path)

    @staticmethod
    def getDeviceLogConfig():
        '''
        Return device log path.
        @rtype: string
        @return: the path of target device log
        '''
        config = ConfigParser.ConfigParser()
        config.read(Parser.SYS_CONFIG_FILE)
        log = config.get('devicelog','log')
        return log

    @staticmethod
    def getSystemConfig():
        '''
        Return system idle time.
        @rtype: SystemConfig
        @return: a instance of SysConfig
        '''
        sysConfig = SystemConfig()
        config = ConfigParser.ConfigParser()
        config.read(Parser.SYS_CONFIG_FILE)
        for item in config.items('time'):
            sysConfig.add(item)
        return sysConfig

    @staticmethod
    def getUserAccountConfig():
        '''
        Return user account info.
        @rtype: Account
        @return: a instance of Account
        '''
        account = Account()
        config = ConfigParser.ConfigParser()
        config.read(Parser.SYS_CONFIG_FILE)
        for item in config.items('user'):
            account.add(item)
        return account

    @staticmethod
    def setUserAccountConfig():
        '''
        Set user account info.
        '''
        account = Account()
        config = ConfigParser.ConfigParser()
        config.read(Parser.SYS_CONFIG_FILE)
        for item in config.items('user'):
            account.add(item)
        return account

def readTestsFromConfigFile(name):
    '''
    Get test case list from test case plan file.
    @type name: string
    @param name: the path of test case plan file
    @rtype: list
    @return: a list of test case
    '''
    if not os.path.exists(name):
        print >>sys.stderr, 'Plan file does not exists.'
        sys.exit(1)

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

'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import os,string,sys
class ConfigParser(object):
    #CONFIG_FILE_NAME = 'plan' 
    @staticmethod
    def readTests(path):
        return readTestsFromConfigFile(path)

    @staticmethod
    def readTestActionConfig(path):
        readTestActionConfigFromFile(path)

def readTestsFromConfigFile(name):
    if not os.path.exists(name):
        print >>sys.stderr, 'Config file does not exist.'
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

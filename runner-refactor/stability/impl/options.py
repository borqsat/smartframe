#!/usr/bin/env python  
#coding: utf-8

'''
Class for options.
python 2.7 or above
'''

import sys, time, os 
import ConfigParser, argparse
from os.path import dirname,abspath,join,exists

__version__ = '0.2'
WORK_SPACE = dirname(dirname(dirname(abspath(__file__))))
USER_CONFIG_FILE = join(WORK_SPACE, 'user.config')
SYSTEM_CONFIG_FILE = join(WORK_SPACE, 'system.config')

class Options(object):

    def __init__(self, argv):
        self._USAGE='python runtest.py --plan path_of_plan --cycle 1000\n'
        self._opt = self.__parse_options().parse_args(argv[1:])

    def __getitem__(self,name):
        if not hasattr(self._opt,name):
            raise KeyError('Non-existing argument \'%s\'' % name) 
        return getattr(self._opt,name)

    def __parse_options(self):
        parser = argparse.ArgumentParser(description='Process the paramters of stability test',
                prog='Stability', usage=self._USAGE)
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--plan', action=self._validate(parser),
                help='Set the relatvie or absolute path of test plan definition file')
        group.add_argument('--testcase', nargs='?',
                help='Set the module path list of test case')
        parser.add_argument('--product', required=True, action=self._validate(parser),
                help='Set the name of the tested product')
        parser.add_argument('-c', '--cycle', type=int, default=1, dest='cycle',
                help='Set the loops of testing. Default is 1.')
        parser.add_argument('--upload', action='store_true',default = True,
                help='Set to upload test result')
        parser.add_argument('--screenmonitor', action='store_true', default=True,
                help='Set to upload test result')
        parser.add_argument('--platform', default='android',
                help='Set to upload test result')
        parser.add_argument('--configfile', type=argparse.FileType('r'), default=join(WORK_SPACE,'system.config'),
                help='read value from config file')
        return parser

    def _validate(self,parser):
        class CheckAction(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                if not exists(join(WORK_SPACE,values)) and not exists(join(os.getcwd(),values)):
                    parser.error('%s file not found!'%values)
                setattr(namespace, self.dest, values)
        return CheckAction

if __name__ == '__main__':
    opt = Options(sys.argv[1:])
    print opt['plan']
    print opt['product']
    print opt['cycle']
    print opt['platform']
    print opt['configfile']
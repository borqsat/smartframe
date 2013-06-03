#!/usr/bin/env python  
#coding: utf-8

'''
New options Class

'''

import sys, time, os 
import ConfigParser, argparse
from os.path import dirname,abspath,join

__version__ = '0.2'

WORK_SPACE = dirname(dirname(dirname(dirname(abspath(__file__)))))
USER_CONFIG_FILE = join(WORK_SPACE, 'user.config')
SYSTEM_CONFIG_FILE = join(WORK_SPACE, 'system.config')

class Options(object):

    def __init__(self, argv):
        self.USAGE="runtest --plan testplan --cycle 1000 \n\
        run test --plan test plan --testcase <testpackage>/<testcase> \n\
        "

        self.opt = self.__parse_options().parse_args(argv)

    def __parse_options(self):
        parser = argparse.ArgumentParser(description='Process the paramters of stability test',
                prog='Stability', usage=self.USAGE)
        parser.add_argument('-p', '--plan', 
                help='Set the test plan')
        parser.add_argument('--product', 
                help='Set the tested product')
        parser.add_argument('-c', '--cycle', type=int, default=1,
                help='Set the loops of testing. Default is 1. ')
        parser.add_argument('--upload', action='store_true',
                help='Set to upload test result')

        return parser
     

if __name__ == '__main__':
    opt = Options(sys.argv[1:]).opt
    print opt.plan
    print opt.product
    print opt.cycle
    print opt.upload
    

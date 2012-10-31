import sys,os,logging
ext_jar_path = '%s/%s' % (os.path.dirname(__file__),'sikuli-script.jar')
sys.path.append(ext_jar_path)
from org.sikuli.script import Finder
from org.sikuli.script import Pattern
from org.sikuli.script import Settings
Settings.InfoLogs = False
__all__ = ['imglib']



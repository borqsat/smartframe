import sys,os,commands
bits = commands.getoutput("getconf LONG_BIT")
jar = '%s%s%s'%('recognition',bits,'.jar')
ext_jar_path = '%s%s%s' % (os.path.dirname(__file__),os.sep,jar)
sys.path.append(ext_jar_path)
from org.sikuli.script import Settings
Settings.InfoLogs = False

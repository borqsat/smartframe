
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
@attention: tested on ubuntu 10.04(32bit b4bit), 11.04(32bit 64bit), 12.04(32 bit)
@bug: None
@warning: None
'''  

import platform,commands,os,sys
OPENCV = ('libcv.so.2.1','libcvaux.so.2.1','libcxcore.so.2.1','libcxts.so.2.1','libhighgui.so.2.1','libml.so.2.1')
ADB_SHELL = 'adb shell '
ADB_VERSION = 'adb version'
WHICH_ADB = 'which adb'
WHICH_SDB = 'which sdb'
SDB_SHELL = 'sdb shell '
SDB_VERSION = 'sdb version'
#Local system information defination
JAVA_VERSION = 'java -version'
OS_VERSION1004 = 'Ubuntu 10.04'
OS_VERSION1104 = 'Ubuntu 11.04'
OS_VERSION1204 = 'Ubuntu 12.04'
JDK6 = '1.6'
JDK7 = '1.7'
ADB_VERSION_INFO = ['Android Debug Bridge version 1.0.26','Android Debug Bridge version 1.0.29','Android Debug Bridge version 1.0.31']
SDB_VERSION_INFO = ['Smart Development Bridge version 2.0.2']
LOCAL_LIB  = '/usr/local/lib/'

'''
Only execute when the first time to run smartRunner on machine.
'''
class SysSetup(object):
    def setup(self):
        self.currentPath = sys.path[0]
        print self.currentPath
        #Verify Operating system. JDK version.
        self.checkTestEnvs()

    #check if Linux OS, JDK version
    def checkTestEnvs(self) :
        print '==========Common set up of system=========='
        #check liunx os version
        print '1.Check os version'
        systemInfo = platform.system()
        print 'OS version:' + systemInfo
        if systemInfo != 'Linux':
            print 'ERROR!  Please install Linux Ubuntu 10.04,11.04 or 12.04'
            sys.exit()
        linuxVersion = commands.getoutput('cat /etc/issue')
        print linuxVersion
        if linuxVersion.find(OS_VERSION1004) == -1 and linuxVersion.find(OS_VERSION1104) and linuxVersion.find(OS_VERSION1204):
            print 'ERROR!  Please install Linux Ubuntu 10.04 ,11.04,or 12.04.'
            #sys.exit()
        print 'SUCCESS!'
        print '------------------------------------------------------'
        
        #check jdk version
        print '2.Check jdk version'
        jdkVersion = commands.getoutput(JAVA_VERSION)
        print jdkVersion
        if jdkVersion.find(JDK6) == -1 and jdkVersion.find(JDK7) == -1:
            print 'ERROR!  Please install jdk 1.6.x or jdk1.7.x'
            sys.exit()
        print 'SUCCESS!'
        print '------------------------------------------------------'

        print '3.Check openCV'
        for f in OPENCV:
            files = '%s%s'%(LOCAL_LIB,f) 
            if not os.path.exists(files):
                self.installOpenCV()
                print 'Opencv Install finished!'
                break
        print 'SUCCESS!'
        print '------------------------------------------------------\n'
        print 'Environment install finished!'
        print '======================================================\n'

                
    def installOpenCV(self):
        print 'Install openCV...'
        bits = commands.getoutput("getconf LONG_BIT")
        cmd = []
        for lib in OPENCV:
            cmd.append('%s/libs/dependence/opencv%sbit/%s ' % (self.currentPath,bits,lib))
        os.popen('%s%s%s' % ('sudo cp ',''.join(cmd),LOCAL_LIB))
        os.popen('%s %s' % ('cd',LOCAL_LIB))
        #os.popen('%s %s' % ('sudo ln -s ','libcvaux.so.2.1 libcvaux.so'))
        os.popen('%s%s%s%s%s' % ('sudo ln -s ',LOCAL_LIB,'libcvaux.so.2.1 ',LOCAL_LIB,'libcvaux.so'))
        #os.popen('%s %s' % ('sudo ln -s ','libcv.so.2.1 libcv.so'))
        os.popen('%s%s%s%s%s' % ('sudo ln -s ',LOCAL_LIB,'libcv.so.2.1 ',LOCAL_LIB,'libcv.so'))
        #os.popen('%s %s' % ('sudo ln -s ','libcxcore.so.2.1 libcxcore.so'))
        os.popen('%s%s%s%s%s' % ('sudo ln -s ',LOCAL_LIB,'libcxcore.so.2.1 ',LOCAL_LIB,'libcxcore.so'))
        
        #os.popen('%s %s' % ('sudo ln -s ','libcxts.so.2.1 libcxts.so'))
        os.popen('%s%s%s%s%s' % ('sudo ln -s ',LOCAL_LIB,'libcxts.so.2.1 ',LOCAL_LIB,'libcxts.so'))
        
        #os.popen('%s %s' % ('sudo ln -s ','libhighgui.so.2.1 libhighgui.so'))
        os.popen('%s%s%s%s%s' % ('sudo ln -s ',LOCAL_LIB,'libhighgui.so.2.1 ',LOCAL_LIB,'libhighgui.so'))
             
        #os.popen('%s %s' % ('sudo ln -s ','libml.so.2.1 libml.so'))
        os.popen('%s%s%s%s%s' % ('sudo ln -s ',LOCAL_LIB,'libml.so.2.1 ',LOCAL_LIB,'libml.so'))
        os.popen('%s %s '% ('sudo ','ldconfig'))
        print 'Env Install finished!'

if (__name__ == '__main__'):
    SysSetup().setup()


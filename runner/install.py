
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
@attention: Linux 32 bit (linux 64 bit not support yet)
@bug: None
@warning: None
'''  
#OpenCV is an excellent library for Computer Vision
import platform,commands,os,sys
OPENCV = ('libcv.so.2.1','libcvaux.so.2.1','libcxcore.so.2.1','libcxts.so.2.1','libhighgui.so.2.1','libml.so.2.1')
ADB_VERSION = 'adb version'
WHICH_ADB = 'which adb'
#Local system information defination
JAVA_VERSION = 'java -version'
OS_VERSION = 'Ubuntu 10.04'
JDK_VERSION = '1.6'
ADB_VERSION_INFO = ['Android Debug Bridge version 1.0.26','Android Debug Bridge version 1.0.29']
LOCAL_LIB  = '/usr/local/lib/'
class SysSetup(object):
    def setup(self):
        self.currentPath = sys.path[0]
        print self.currentPath
        #Verify Operating system. JDK version. Adb version.SDK MonkeyRunner path
        self.checkTestEnvs()

    #check if Linux OS, JDK, ADB, and Monkeyrunner work
    def checkTestEnvs(self) :
        #check liunx os version
        print '1.Check os version'
        systemInfo = platform.system()
        print 'OS version:' + systemInfo
        if systemInfo != 'Linux':
            print 'ERROR!  Please install Linux Ubuntu 10.04'
            sys.exit()
        linuxVersion = commands.getoutput('cat /etc/issue')
        print linuxVersion
        if linuxVersion.find(OS_VERSION) == -1:
            print 'ERROR!  Please install Linux Ubuntu 10.04'
            #sys.exit()
        print 'SUCCESS!'
        print '------------------------------------------------------'
        
        #check jdk version
        print '2.Check jdk version'
        jdkVersion = commands.getoutput(JAVA_VERSION)
        print jdkVersion
        if jdkVersion.find(JDK_VERSION) == -1:
            print 'ERROR!  Please install jdk 1.6'
            sys.exit()
        print 'SUCCESS!'
        print '------------------------------------------------------'
        
        #check adb set to environment varible
        print '3.Check adb set to environment variable'
        adbEnv = commands.getoutput(WHICH_ADB)
        print adbEnv
        if adbEnv.find('/home') and adbEnv.find('adb') == -1:
            print 'ERROR!  Please set adb to environment variable!'
            sys.exit()
        print 'SUCCESS!'
        print '------------------------------------------------------'
        
        #check adb version
        print '4.Check adb version...'
        adbVer = commands.getoutput(ADB_VERSION)
        print adbVer
        if not adbVer in ADB_VERSION_INFO:
            print 'ERROR!  Please use 2.3.3 or 4.0.x adb version '
            sys.exit()
        print 'SUCCESS!'
        print '------------------------------------------------------'
        
        #check monkeyrunner set to environment
        print '5.Check monkeyrunner set to environment variable'
        monkeyrunnerEnv = commands.getoutput('which monkeyrunner')
        print monkeyrunnerEnv
        if monkeyrunnerEnv.find('/home') and monkeyrunnerEnv.find('monkeyrunner') == -1:
            print 'ERROR!  Please set monkeyrunner to environment variable'
            sys.exit()
        print 'SUCCESS!'
        print '------------------------------------------------------'

        print '6.Check openCV'
        for f in OPENCV:
            files = '%s%s'%(LOCAL_LIB,f) 
            if not os.path.exists(files):
                self.installOpenCV()
                print 'Opencv Install finished!'
                break
        print 'SUCCESS!'
        print '------------------------------------------------------\n'
        print 'Environment install finished!'
                
    def installOpenCV(self):
        print 'Install...'
        cmd = []
        for lib in OPENCV:
            cmd.append('%s/install/opencv/%s ' % (self.currentPath,lib))
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


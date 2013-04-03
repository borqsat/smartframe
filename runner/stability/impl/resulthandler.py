'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import os,shutil,thread,threading,time,zipfile,sys
from signal import signal, SIGINT,SIGTSTP
from libs.pubsub import pub
from stability.util.log import Logger
from builder import TestBuilder
from uploader import ResultSender,Sender
from configparser import Parser
import device

LOG_FILE = Parser.getDeviceLogConfig()

#notify server client exited and resource released.
def stop(signum, frame):
    '''Method for ctaching CTRL+C CTRL+D event'''
    if ResultHandler.sender:
        if ResultSender.getInstance().queue:
            pub.sendMessage('collectresult',sessionStatus='sessionstop')
            task_wait = ResultSender.getInstance().queue
            if not task_wait.empty():
                task_wait.mutex.acquire()
                try:
                    task_wait.queue.clear()
                    task_wait.unfinished_tasks = 0
                    task_wait.not_full.notify()
                    task_wait.all_tasks_done.notifyAll()
                finally:
                    task_wait.mutex.release()            
        ResultHandler.sender.stop()
    sys.exit()

class ResultHandler(object):
    '''
    A class for handling test result.
    '''
    sender = None
    is_upload = None
    def handle(self,info=None,path=None,sessionStatus=None):
        '''Dispatch the test results'''
        if not ResultHandler.is_upload:
            ResultHandler.is_upload = TestBuilder.getBuilder().getProperty('uploadresult')
            #if ResultHandler.is_upload:
            #    signal(SIGINT, stop)
        if ResultHandler.is_upload and not ResultHandler.sender:
            ResultHandler.sender = Sender(ResultSender.getInstance().queue)
            ResultHandler.sender.setDaemon(True)
            ResultHandler.sender.start()
        handleResult(info,path,sessionStatus,ResultHandler.is_upload)
        #print '************************************************************'
        #handler = Handler(info,path,sessionStatus,_isUpload)
        #handler.start()
        #handler.join()

class Handler(threading.Thread):
    def __init__(self,info,path,sessionStatus,isUpload):
        threading.Thread.__init__(self)
        self.info = info
        self.path = path
        self.sessionStatus = sessionStatus
        self.isUpload = isUpload

    def run(self):
        handleResult(self.info,self.path,self.sessionStatus,self.isUpload)

def handleResult(info,path,sessionStatus,isUpload):
    '''Sort test case result in workspace folder.
    Arguments:
    @type info:tuple
    @params info:tuple of test case object description.(should not be none)
    @type path:string
    @params path:the file path need to be uploaded.
    @type sessionStatus:string
    @params sessionStatus: the test session status (start,stop)
    @type isUpload:boolean
    @params isUpload:the switch of uploading function.
    '''
    logger = Logger.getLogger()
    if info:
        if  info[0] in ['addFailure','addError']:
            case_name = '%s.%s' %(type( info[1][1]).__name__,  info[1][1]._testMethodName)
            case_starttime = info[1][0].case_start_time
            testcase_result_folder = '%s-%s'%(case_name,case_starttime)
            report_path = os.path.join(TestBuilder.getBuilder().getWorkspace(),'report')
            #result_path = os.path.join(report_path,'result-%s' % TestBuilder.getBuilder().getProperty('starttime'))
            result_path = os.path.join(report_path,'%s-%s' % (TestBuilder.getBuilder().getProperty('product'),TestBuilder.getBuilder().getProperty('starttime')))
            src =  os.path.join(os.path.join(result_path,'all'),testcase_result_folder)
            if info[0] == 'addFailure':
                logger.debug('handle test failure...')
                dest = os.path.join(os.path.join(result_path,'fail',testcase_result_folder))
            elif info[0] == 'addError':
                logger.debug('handle test error...')
                dest = os.path.join(os.path.join(result_path,'error',testcase_result_folder))
            if (src is not None and dest is not None):
                flag =  _copyFilesToOtherFolder(src, dest,info[1][1])
                f = False
                if flag:
                    f = _saveLog(dest)
                if f:
                    zipLog(testcase_result_folder,dest)

        if isUpload:
            ResultSender.getInstance().addTask(info=info)
    elif path:
        if isUpload:
            ResultSender.getInstance().addTask(path=path)
    elif sessionStatus:
        if isUpload:
            ResultSender.getInstance().addTask(sessionStatus=sessionStatus)

def zipFolder(foldername, filename, includeEmptyDIr=True):
    empty_dirs = []
    try:  
        ziper = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)  
        for root, dirs, files in os.walk(foldername):  
            empty_dirs.extend([d for d in dirs if os.listdir(os.path.join(root, d)) == []])  
            for name in files:
                ziper.write(os.path.join(root ,name),root)
            if includeEmptyDIr:  
                for d in empty_dirs:  
                    zif = zipfile.ZipInfo(os.path.join(root, d) + "/")  
                    ziper.writestr(zif, "")
            empty_dirs = []
        return True
    except:
        return False
    finally:
        if ziper != None:
            ziper.close()

def zipLog(name,dest):
    logfolder = os.path.join(dest,'device_log')
    zipName = '%s%s%s.%s' % (dest,os.sep,name,'zip')
    zipFolder(logfolder,zipName)

def _copyFilesToOtherFolder(src, dest,info):
    '''Copy test failures or error case from source folder to destination folder.
    Keyword arguments:
    src -- Path of source folder. (should not be none)
    dest -- Path of destination folder(should not be none)
    '''
    try:
        rightPath = info.verifier.expectResult.getCurrentCheckPoint()
        shutil.copytree(src, dest)
        shutil.copy2(rightPath,dest)
        ##add test.log to failure folder
        logfolder = '%s%s%s%s' % (os.path.dirname(os.path.dirname(os.path.dirname(__file__))),os.sep,'log',os.sep)
        debuglog1 = '%s%s' % (logfolder,'test.log')
        debuglog2 = '%s%s' % (logfolder,'test.log.1')
        if os.path.exists(debuglog1):
            shutil.copy2(debuglog1,dest)
        if os.path.exists(debuglog2):
            shutil.copy2(debuglog2,dest)           
        return True
    except:
        return False


def _saveLog(dest):
    '''Generate device log in destination folder.
    Keyword arguments:
    dest -- Path of destination folder(should not be none)
     '''
    try:
        logfolder = os.path.join(dest, 'device_log')
        os.makedirs(logfolder)
        #adbPull('/data/logs/aplog;/data/logs/aplog.1;/data/anr/traces.txt;',logfolder)
        if str(sys.path).find('tizenrunner') != -1:
            _sdbPull(LOG_FILE,logfolder)
        else:
            _adbPull(LOG_FILE,logfolder)
        return True
    except:
        return False

def _adbPull(pullfiles,folder):
    serialId = device._getSerial()
    if pullfiles is not None and pullfiles is not '':
        files = pullfiles.replace(',', ';')
        files = files.split(';')
        for file in files:
            file = file.strip()
            if file is not '':
                destfile = os.path.join(folder, os.path.basename(file))
                if not serialId:
                    cmd = '%s %s %s %s %s' % ('adb', 'pull', file, destfile, '2>/dev/null')
                else:
                    cmd = '%s %s %s %s %s %s %s' % ('adb', '-s',serialId,'pull', file, destfile, '2>/dev/null')
                ret = os.system(cmd)
    return True

def _sdbPull(pullfiles,folder):
    serialId = device._getSerial()
    if pullfiles is not None and pullfiles is not '':
        files = pullfiles.replace(',', ';')
        files = files.split(';')
        for file in files:
            file = file.strip()
            if file is not '':
                destfile = os.path.join(folder, os.path.basename(file))
                if not serialId:
                    cmd = '%s %s %s %s %s' % ('sdb', 'pull', file, destfile, '2>/dev/null')
                else:
                    cmd = '%s %s %s %s %s %s %s' % ('sdb', '-s',serialId,'pull', file, destfile, '2>/dev/null')
                ret = os.system(cmd)
    return True

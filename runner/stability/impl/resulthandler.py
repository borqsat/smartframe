from stability.util.log import Logger
from builder import TestBuilder
from uploader import ResultSender,Sender
import os,shutil,thread,threading
from pubsub import pub
import time,zipfile,os
  
class ResultHandler(object):
    sender = None
    def __init__(self):
        pass

    #@staticmethod
    def handle(self,info=None,path=None,sessionStatus=None):
        _isUpload = TestBuilder.getBuilder().getProperty('uploadresult')
        _isLocal = True
        if _isUpload and not ResultHandler.sender:
            ResultHandler.sender = Sender(ResultSender.getInstance().queue)
            ResultHandler.sender.start()
        handleResult(info,path,sessionStatus,_isUpload)
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
    '''Sort test case result from "all" folder.
    Keyword arguments:
    info -- tuple of test case object description.(should not be none)
    '''
    logger = Logger.getLogger()
    if info:
        if  info[0] in ['addFailure','addError']:
            case_name = '%s.%s' %(type( info[1][1]).__name__,  info[1][1]._testMethodName)
            case_starttime = info[1][0].case_start_time
            testcase_result_folder = '%s-%s'%(case_name,case_starttime)
            result_path = os.path.join(TestBuilder.getBuilder().getWorkspace(),'result-%s'%TestBuilder.getBuilder().getProperty('starttime'))
            src =  os.path.join(os.path.join(result_path,'all'),testcase_result_folder)
            if info[0] == 'addFailure':
                logger.debug('distribute add failed')
                dest = os.path.join(os.path.join(result_path,'fail',testcase_result_folder))
            elif info[0] == 'addError':
                logger.debug('distribute add error:')
                dest = os.path.join(os.path.join(result_path,'error',testcase_result_folder))
            if (src is not None and dest is not None):
                flag =  _copyFilesToOtherFolder(src, dest)
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
    except:
        pass
    finally:
        ziper.close()  

def zipLog(name,dest):
    logfolder = os.path.join(dest,'log')
    zipName = '%s/%s.%s'%(dest,name,'zip')
    zipFolder(logfolder,zipName)

def _copyFilesToOtherFolder(src, dest):
    '''Copy test failures or error case from source folder to destination folder.
    Keyword arguments:
    src -- Path of source folder. (should not be none)
    dest -- Path of destination folder(should not be none)
     '''
    try:
        shutil.copytree(src, dest)
        return True
    except:
        return False


def _saveLog(dest):
    '''Generate device log in destination folder.
    Keyword arguments:
    dest -- Path of destination folder(should not be none)
     '''
    try:
        logfolder = os.path.join(dest, 'log')
        os.makedirs(logfolder)
        #adbPull('/data/logs/aplog;/data/logs/aplog.1;/data/anr/traces.txt;',logfolder)
        _adbPull('/data/logs/aplog;/data/logs/aplog.1;/data/logs/aplog.2',logfolder)
        return True
    except:
        return False

def _adbPull(pullfiles,folder):
    if pullfiles is not None and pullfiles is not '':
        files = pullfiles.replace(',', ';')
        files = files.split(';')
        for file in files:
            file = file.strip()
            if file is not '':
                destfile = os.path.join(folder, os.path.basename(file))
                #TODO: subprocess.Popen leask fds, so...
                #process = subprocess.Popen(['adb', 'pull', file, destfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #process.wait()
                cmd = "%s %s %s %s %s" % ('adb', 'pull', file, destfile, '2>/dev/null')
                ret = os.system(cmd)
    return True

from stability.util.log import Logger
from builder import TestBuilder
from uploader import ResultSender
import os,shutil

class ResultHandler(object):

    def __init__(self):
        pass

    @staticmethod
    def handle(info=None,path=None):
        #load test setting
        _isUpload = TestBuilder.getBuilder().isUploadResult()
        _isLocal = TestBuilder.getBuilder().isLocalResult()
        if info:
            _sortTestCaseResult(info)
        if _isUpload:
            ResultSender.getInstance().addTask(info,path) 
        if _isLocal:
            pass

def _sortTestCaseResult(info):
    '''Sort test case result from "all" folder.
    Keyword arguments:
    info -- tuple of test case object description.(should not be none)
     '''
    logger=Logger.getLogger()
    #logger.debug('copy failures result to fail or error folder')
    #logger.debug('name:'+info[1][1]._testMethodName+' time:'+info[1][1].starttime)
    if not info[0] in ['addFailure','addError']:
        return 
    case_name = '%s.%s' %(type( info[1][1]).__name__,  info[1][1]._testMethodName)
    case_starttime = info[1][1].starttime
    testcase_result_folder = '%s-%s'%(case_name,case_starttime)
    result_path = os.path.join(TestBuilder.getBuilder().getWorkspace(),'result-%s'%TestBuilder.getBuilder().getStartTime())
    src =  os.path.join(os.path.join(result_path,'all'),testcase_result_folder)
    if info[0] == 'addFailure':
        #logger.debug('distribute add failed')
        dest = os.path.join(os.path.join(result_path,'fail',testcase_result_folder))
    elif info[0] == 'addError':
        #logger.debug('distribute add error:')
        dest = os.path.join(os.path.join(result_path,'error',testcase_result_folder))
    if (src is not None and dest is not None):
        _copyFilesToOtherFolder(src, dest)
        _saveLog(dest)

def _copyFilesToOtherFolder(src, dest):
    '''Copy test failures or error case from source folder to destination folder.
    Keyword arguments:
    src -- Path of source folder. (should not be none)
    dest -- Path of destination folder(should not be none)
     '''
    try:
        shutil.copytree(src, dest)
    except shutil.Error, err:
        pass


def _saveLog(dest):
    '''Generate device log in destination folder.
    Keyword arguments:
    dest -- Path of destination folder(should not be none)
     '''
    try:
        logfolder = os.path.join(dest, 'log')
        os.makedirs(logfolder)
        #adbPull('/data/logs/aplog;/data/logs/aplog.1;/data/anr/traces.txt;',logfolder)
        _adbPull('/data/logs',logfolder)
    except Exception,e:
        pass

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
                os.system(cmd)
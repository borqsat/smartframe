import datetime,traceback,time,zipfile,os,shutil,threading,uuid,Queue
import urllib2
from stability.util.log import Logger
import minjson
from builder import TestBuilder
from devicemanager import DeviceManager


def _openFile(path):
    f = None
    try: 
        f = open(path, "rb")
        data = f.read()
        return data
    except:
        return ''
    finally:
        if f != None:
            f.close()

def zipFolder(foldername, filename, includeEmptyDIr=True):   
    empty_dirs = []  
    ziper = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)  
    for root, dirs, files in os.walk(foldername):  
        empty_dirs.extend([d for d in dirs if os.listdir(os.path.join(root, d)) == []])  
        for name in files:  
            ziper.write(os.path.join(root ,name))  
        if includeEmptyDIr:  
            for d in empty_dirs:  
                zif = zipfile.ZipInfo(os.path.join(root, d) + "/")  
                ziper.writestr(zif, "")
        empty_dirs = []  
    ziper.close()  


class SendUtils(object):
    _server_url = 'http://192.168.7.212:8081'
    _session_create_url = _server_url+'/test/session/%s/create'
    _caseresult_create_url = _server_url+'/test/caseresult/%s/%s/create'
    _caseresult_update_url = _server_url+'/test/caseresult/%s/%s/update'
    _upload_file_url = _server_url+'/test/caseresult/%s/%s/fileupload'

    @staticmethod
    def request(task):
        logger = Logger.getLogger()
        url = task['url']
        content_type = task['content_type']
        method = task['method']
        postdata = task['data']
        logger.debug('url:'+url+' type:'+content_type+' method:'+method)        
        #SendUtils._doCommonRequest(url=_url,postdata=_data,content_type='image/png',method='PUT')
        SendUtils._doCommonRequest(url,postdata,content_type,method)

    @staticmethod
    def _doCommonRequest(url,postdata,content_type,method):
        '''
           Transmit a data to remote server using HTTP(GET,POST,PUT).
           and got a response which specified by JSON formate : "{"results":"content"}" from remote server.
           @poastdata String of json formate or the binary data of zip,png
           @return dictionary of response
           @Exception URLError.
        '''
        logger = Logger.getLogger()
        #user define exception
        errorcode = {'unspecified':31,
                     'feedback_ok':32,
                     'feedback_fail':33,
                     'json_error_attr':34,
                     'json_error_format':35
                     }
        f = None
        try:
            logger.debug('init request!')
            request = urllib2.Request(url)
            if method == 'POST':
                postdata['token'] = '1122334455667788'
                jsonstr = minjson.write(postdata)
                logger.debug(jsonstr)
                request.add_data(jsonstr)
            else:
                request.add_header('token','1122334455667788')
                request.add_data(postdata)                
            #the content type of data application/json application/zip image/png
            logger.debug('add content_type!')            
            request.add_header('Content-Type',content_type)
            #the content type of feedback from server
            logger.debug('add Accept!')
            request.add_header('Accept', 'application/json')
            #the length of data
            #logger.debug('add Content-Length!')
            #request.add_header("Content-Length", str(len(postdata)))
            #the http request type GET POST PUT
            logger.debug('add method!')
            request.get_method = lambda: method
            urllib2.socket.setdefaulttimeout(10)
            logger.debug('open the url!')
            f = urllib2.urlopen(request)
            json_feedback = f.read()
            dic = eval(json_feedback)
            #key = list(dic).pop()
            #value = str(dic[key])
            return dic

        except Exception,e:
            #all exception.urllib2.URLError: <urlopen error timed out>...
            logger.debug('Do http request, got error!')
            return ''
        finally:
            if f != None:
                f.close()

class ResultSender(object):
    '''Class for upload data to server.Support JSON and application/zip and image/png.
    '''
    __instance = None 
    __mutex = threading.Lock()

    def __init__(self):
        self.logger= Logger.getLogger()
        self.tid = 0
        self.queue = Queue.Queue()
        self.sessionId = str(uuid.uuid1())
        self.queue.put(ResultSender.parseMessage(msg_type='sessiondata',session_id=self.sessionId))
        Sender(self.queue).start()

    @staticmethod
    def getInstance(argv=None):
        '''Return single instance of ResultSender.
        '''
        if(ResultSender.__instance == None): 
            ResultSender.__mutex.acquire()
            if(ResultSender.__instance == None):
                ResultSender.__instance = ResultSender()
            else: 
                pass
            ResultSender.__mutex.release() 
        else:
            pass
     
        return ResultSender.__instance

    def addTask(self,info=None,path=None):
        '''Add test result info to queue
        @params:
        info: tuple of test case. (testmethodname,object of test case,object of trace info)
        path: the upload file resource path
        '''
        if info:
            if info[0]=='startTest':
                #creat case result id when start test
                self.tid += 1
        msg = ResultSender.parseMessage(msg_type='caseresult',session_id=self.sessionId,caseresult_id=self.tid,test_info=info,file_path=path)
        for task in msg:
            self.queue.put(task)

    @staticmethod
    def parseMessage(msg_type=None,session_id=None,caseresult_id=None,test_info=None,file_path=None):
        logger = Logger.getLogger()
        if msg_type == 'sessiondata':
            logger.debug('********************session request***********************')
            url = SendUtils._session_create_url % session_id
            sessionStarttime = TestBuilder.getBuilder().getStartTime()
            deviceId = DeviceManager.getInstance().getDevice().getDeviceId()
            properties = DeviceManager.getInstance().getDevice().getDeviceInfo()
            logger.debug('********************session starttime*********************'+sessionStarttime)
            postData = {'planname':'plan','starttime':sessionStarttime,'deviceid':deviceId,'deviceinfo':properties}
            contentType = 'application/json'
            method = 'POST'            
            return {'url':url,'data':postData,'content_type':contentType,'method':method}
        if msg_type == 'caseresult':
            logger.debug('********************case result*********************')
            sid = session_id
            tid = caseresult_id
            info = test_info
            path = file_path
            if info:
                if info[0] == 'startTest':
                    logger.debug('********************start test*********************')
                    url = (SendUtils._caseresult_create_url) % (sid,tid)
                    caseName = info[1][1]._testMethodName
                    startTime = time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time()))
                    postData = {'casename':caseName,'starttime':startTime}
                    contentType = 'application/json'
                    method = 'POST'            
                    return [{'url':url,'data':postData,'content_type':contentType,'method':method}]
                elif info[0] == 'addSuccess':
                    logger.debug('********************add success***********************')
                    url = (SendUtils._caseresult_update_url) % (sid,tid)
                    _time = time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time()))
                    postData = {'result':'pass','time':_time}
                    contentType = 'application/json'
                    method = 'POST'
                    return [{'url':url,'data':postData,'content_type':contentType,'method':method}]
                elif info[0] == 'addFailure':
                    logger.debug('********************add failure***********************')
                    resultUrl = (SendUtils._caseresult_update_url) % (sid,tid)
                    resultTime = time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time()))
                    resultPostData = {'result':'fail','time':resultTime}
                    resultContentType = 'application/json'
                    resultMethod = 'POST'
                    resultRequest = {'url':resultUrl,'data':resultPostData,'content_type':resultContentType,'method':resultMethod}
                    #log file
                    logUrl = (SendUtils._upload_file_url) % (sid,tid)
                    logfolder = os.path.join(info[1][1].worker.store.getFailDir(),'log')
                    zipName = '%s_%s.%s'%(sid,tid,'zip')
                    zipFolder(logfolder,zipName)
                    logPostData = _openFile(zipName)
                    logContentType = 'application/zip'
                    logMethod = 'PUT'
                    fileRequest = {'url':logUrl,'data':logPostData,'content_type':logContentType,'method':logMethod}
                    return [resultRequest,fileRequest]

                elif info[0] == 'addError':
                    logger.debug('********************add error***********************')
                    resultUrl = (SendUtils._caseresult_update_url) % (sid,tid)
                    resultTime = time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time()))
                    resultPostData = {'result':'error','time':resulTime}
                    resultContentType = 'application/json'
                    resultMethod = 'POST'
                    resultRequest = {'url':resultUrl,'data':resultPostData,'content_type':resultContentType,'method':resultMethod}
                    #log file
                    #logUrl = (SendUtils._upload_file_url) % (sid,tid)
                    #logfolder = os.path.join(info[1][1].device.workspace_result_fail,'log')
                    #zipName = '%s_%s.%s'%(sid,tid,'zip')
                    #zipFolder(logfolder,_zipname)
                    #logPostData = _openFile(_zipname)
                    #logContentType = 'application/zip'
                    #logMethod = 'PUT'
                    #fileRequest = {'url':logUrl,'data':logPostData,'content_type':logContentType,'method':logMethod}
                    return [resultRequest]
            elif file_path:
                logger.debug('********************upload snapshot***********************')
                sid = session_id
                tid = caseresult_id
                url = (SendUtils._upload_file_url) % (sid,tid)
                postData = _openFile(file_path)
                contentType = 'image/png'
                method = 'PUT'
                return [{'url':url,'data':postData,'content_type':contentType,'method':method}]

class Sender(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.task_queue = q
        self.logger = Logger.getLogger()
        
    def run(self):
        while True:
            if self.task_queue.qsize() > 0:
                job = self.task_queue.get()
                #if don't get tid from server. can create thread for each request.
                self.logger.debug('******sender thread got a task********')
                SendUtils.request(job)
                self.task_queue.task_done()
                self.logger.debug('******sender thread finished a task********')


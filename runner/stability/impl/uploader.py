import datetime,traceback,time,os,shutil,threading,uuid,Queue,hashlib,urllib2
from stability.util.log import Logger
from builder import TestBuilder
from devicemanager import DeviceManager
import minjson

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

class SendUtils(object):
    _server_url = 'http://192.168.7.212:8081'
    _session_create_url = _server_url + '/test/session/%s/create'
    _session_update_url = _server_url + '/test/session/%s/update'
    _caseresult_create_url = _server_url + '/test/caseresult/%s/%s/create'
    _caseresult_update_url = _server_url + '/test/caseresult/%s/%s/update'
    _upload_file_url = _server_url + '/test/caseresult/%s/%s/fileupload'
    _auth_url = 'http://192.168.7.212:8080/user/auth'
    _auth_field = {'appid':'01','username':'borqsat','password':'654321'}

    @staticmethod
    def request(task):
        logger = Logger.getLogger()
        url = task['url']
        content_type = task['content_type']
        method = task['method']
        postdata = task['data']
        exttype = ''
        if task.has_key('exttype'):
            exttype = task['exttype']
            #exttype = '{left:1,top:2,width:3:height:4}'
        logger.debug('url:'+url+' type:'+content_type+' method:'+method+'exttype: '+ exttype)   
        SendUtils._doCommonRequest(url,postdata,content_type,method,exttype)

    @staticmethod
    def _doCommonRequest(url,postdata,content_type,method,ext_type=None):
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
                postdata['token'] = ResultSender.getInstance().token
                jsonstr = minjson.write(postdata)
                logger.debug(jsonstr)
                request.add_data(jsonstr)
            else:
                request.add_header('token',ResultSender.getInstance().token)
                request.add_data(postdata)
            #the content type of data application/json application/zip image/png
            logger.debug('add content_type!')
            request.add_header('Content-Type',content_type)
            #add picture type expect img or the img of error screen 
            request.add_header('Ext-Type',ext_type)
            #the content type of feedback from server
            logger.debug('add Accept!')
            request.add_header('Accept', 'application/json')
            #the length of data
            #request.add_header("Content-Length", str(len(postdata)))
            #the http request type GET POST PUT
            logger.debug('add method!')
            request.get_method = lambda: method
            urllib2.socket.setdefaulttimeout(10)
            logger.debug('open the url!')
            f = urllib2.urlopen(request)
            #headers = f.info()
            #print headers
            json_feedback = f.read()
            #print json_feedback
            return json_feedback

        except Exception,e:
            #all exception.urllib2.URLError: <urlopen error timed out>...
            self.logger.debug(e)
            #logger.debug('Do http request, got error: ' + e)
            return
        finally:
            if f != None:
                urllib2.socket._closeActiveSockets()
                f.close()

class ResultSender(object):
    '''Class for upload data to server.Support JSON and application/zip and image/png.
    '''
    __instance = None 
    __mutex = threading.Lock()

    def __init__(self):
        self.logger = Logger.getLogger()
        self.tid = 0
        self.queue = Queue.Queue()
        self.sessionId = str(uuid.uuid1())
        self.token = self.getToken()
        assert self.token,'token is none'
        self.addTask(sessionStatus='sessionstart')

    def getToken(self):
        field = SendUtils._auth_field
        m = hashlib.md5()
        m.update(field['password'])
        pwd = m.hexdigest()
        url = '%s?%s=%s&%s=%s&%s=%s' % (SendUtils._auth_url,'appid',field['appid'],'username',field['username'],'password',pwd)
        if url:
            f = None
            try:
                urllib2.socket.setdefaulttimeout(10)
                f = urllib2.urlopen(url)
                json_feedback = f.read()
                dic = eval(json_feedback)
                value = dic['results']['token']
                return value
            except:
                return None
            finally:
                if f != None:
                    urllib2.socket._closeActiveSockets()
                    f.close()

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

    def addTask(self,info=None,path=None,sessionStatus=None):
        '''Add test result info to queue
        @params:
        info: tuple of test case. (testmethodname,object of test case,object of trace info)
        path: the upload file resource path
        '''
        if sessionStatus:
            msg = ResultSender.parseMessage(msg_type=sessionStatus,session_id=self.sessionId) 
        elif info:
            if info[0]=='startTest':
                #creat case result id when start test
                self.tid += 1
            msg = ResultSender.parseMessage(msg_type='caseresult',session_id=self.sessionId,caseresult_id=self.tid,test_info=info,file_path=path)
        elif path:
            msg = ResultSender.parseMessage(msg_type='caseresult',session_id=self.sessionId,caseresult_id=self.tid,test_info=info,file_path=path)
 
        for task in msg:
            self.logger.debug(task['url'])
            self.queue.put(task)

    @staticmethod
    def parseMessage(msg_type=None,session_id=None,caseresult_id=None,test_info=None,file_path=None):
        logger = Logger.getLogger()
        if msg_type == 'sessionstart':
            logger.debug('********************session start request***********************')
            url = SendUtils._session_create_url % session_id
            sessionStarttime = TestBuilder.getBuilder().getProperty('starttime')
            deviceId = DeviceManager.getInstance().getDevice().getDeviceId()
            properties = DeviceManager.getInstance().getDevice().getDeviceInfo()
            logger.debug('********************session starttime*********************'+sessionStarttime)
            postData = {'planname':'plan','starttime':sessionStarttime,'deviceid':deviceId,'deviceinfo':properties}
            contentType = 'application/json'
            method = 'POST'            
            return [{'url':url,'data':postData,'content_type':contentType,'method':method}]
        if msg_type == 'sessionstop':
            logger.debug('********************session end request***********************')
            url = SendUtils._session_update_url % session_id
            sessionEndtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            logger.debug('********************session end time*********************'+sessionEndtime)
            postData = {'endtime':sessionEndtime}
            contentType = 'application/json'
            method = 'POST'            
            return [{'url':url,'data':postData,'content_type':contentType,'method':method}]

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
                    #startTime = time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time()))
                    startTime = info[1][0].case_start_time
                    postData = {'casename':caseName,'starttime':startTime}
                    contentType = 'application/json'
                    method = 'POST'            
                    return [{'url':url,'data':postData,'content_type':contentType,'method':method}]
                elif info[0] == 'addSuccess':
                    logger.debug('********************add success***********************')
                    url = (SendUtils._caseresult_update_url) % (sid,tid)
                    _time = time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time()))
                    postData = {'result':'pass','time':_time,'traceinfo':'N/A'}
                    contentType = 'application/json'
                    method = 'POST'
                    return [{'url':url,'data':postData,'content_type':contentType,'method':method}]
                elif info[0] == 'addFailure':
                    logger.debug('********************add failure***********************')
                    resultUrl = (SendUtils._caseresult_update_url) % (sid,tid)
                    resultTime = time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time()))
                    traceInfo = ResultSender._trace_to_string((info[1][2],info[1][1]))
                    resultPostData = {'result':'fail','time':resultTime,'traceinfo':traceInfo}
                    resultContentType = 'application/json'
                    resultMethod = 'POST'
                    resultRequest = {'url':resultUrl,'data':resultPostData,'content_type':resultContentType,'method':resultMethod}
                    #log file
                    url = (SendUtils._upload_file_url) % (sid,tid)
                    #logfolder = os.path.join(info[1][1].worker.store.getFailDir(),'log')
                    case_name = '%s.%s' %(type( info[1][1]).__name__,  info[1][1]._testMethodName)
                    case_starttime = info[1][0].case_start_time
                    testcase_result_folder = '%s-%s'%(case_name,case_starttime)
                    result_path = os.path.join(TestBuilder.getBuilder().getWorkspace(),'result-%s'%TestBuilder.getBuilder().getProperty('starttime'))      
                    dest = os.path.join(os.path.join(result_path,'fail',testcase_result_folder))
                    zipName = '%s.%s'%(testcase_result_folder,'zip')
                    logPath = os.path.join(dest,zipName)
                    logPostData = _openFile(logPath)
                    logContentType = 'application/zip'
                    logMethod = 'PUT'
                    failFileRequest = {'url':url,'data':logPostData,'content_type':logContentType,'method':logMethod}
                    logger.debug('except file path: ')
                    rightPath = info[1][1].checker.expectResult.getCurrentCheckPoint()
                    rightPostData = _openFile(rightPath)
                    expectFileRequest = {'url':url,'data':rightPostData,'content_type':'image/png','method':'PUT','exttype':'expect'}
                    logger.debug('********************end failure***********************')
                    return [resultRequest,failFileRequest,expectFileRequest]

                elif info[0] == 'addError':
                    logger.debug('********************add error***********************')
                    resultUrl = (SendUtils._caseresult_update_url) % (sid,tid)
                    resultTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    traceInfo = ResultSender._trace_to_string((info[1][2],info[1][1]))
                    resultPostData = {'result':'error','time':resultTime,'traceinfo':traceInfo}
                    resultContentType = 'application/json'
                    resultMethod = 'POST'
                    resultRequest = {'url':resultUrl,'data':resultPostData,'content_type':resultContentType,'method':resultMethod}
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

    @classmethod
    def _trace_to_string(cls,traceinfo):
        '''Converts err,test into a string as trace log.'''
        if not isinstance(traceinfo,tuple):
            return traceinfo
        exctype, value, tb = traceinfo[0]
        # Skip test runner traceback levels
        while tb and  ResultSender._is_relevant_tb_level(tb):
            tb = tb.tb_next
        if exctype is traceinfo[1].failureException:
            # Skip assert*() traceback levels
            length =  ResultSender._count_relevant_tb_levels(tb)
            return ''.join(traceback.format_exception(exctype, value, tb, length))
        return ''.join(traceback.format_exception(exctype, value, tb))

    @classmethod
    def _is_relevant_tb_level(cls,tb):
            return '__unittest' in tb.tb_frame.f_globals

    @classmethod
    def _count_relevant_tb_levels(cls,tb):
            length = 0
            while tb and not ResultSender._is_relevant_tb_level(tb):
                length += 1
                tb = tb.tb_next
            return length

class Sender(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.isStop = False
        self.task_queue = q
        self.logger = Logger.getLogger()

    def run(self):
        while not self.isStop:
            if self.task_queue.qsize() > 0:
                job = self.task_queue.get()
                #if don't get tid from server. Can create thread for each request.
                try:
                    self.logger.debug('******sender thread got a task********')
                    SendUtils.request(job)
                    self.logger.debug('******sender thread finished a task********')
                finally:
                    self.task_queue.task_done()

    def stop(self):
        self.isStop = True

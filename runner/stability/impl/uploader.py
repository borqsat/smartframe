'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import datetime,traceback,time,os,shutil,threading,uuid,Queue,hashlib,urllib2
from stability.util.log import Logger
from builder import TestBuilder
from devicemanager import DeviceManager
from configparser import Parser
import minjson

def _openFile(path):
    '''Get binary data of file'''
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
    '''Send http request functions'''
    @staticmethod
    def request(task):
        '''
        Static method for uploading the data to server.
        data format: 
        {'url':url,'data':rightFullData,'content_type':'image/png','method':'PUT','exttype':'userdefine'}
        '''
        logger = Logger.getLogger()
        url = task['url']
        content_type = task['content_type']
        method = task['method']
        postdata = task['data']
        exttype = ''
        if task.has_key('exttype'):
            exttype = task['exttype']
            #exttype = '{left:1,top:2,width:3:height:4}'
            logger.debug('url:'+url+' type:'+content_type+' method:'+method+' exttype: '+ exttype)
            return SendUtils._doHttpRequest(url,postdata,content_type,method,ext_type=exttype)
        else:
            return SendUtils._doHttpRequest(url,postdata,content_type,method)

    @staticmethod
    def _doHttpRequest(url,postdata,content_type,method,ext_type=None):
        '''
           Transmit a data to remote server using HTTP(GET,POST,PUT).
           and got a response which specified by JSON formate : "{"results":"content"}" from remote server.
           @poastdata String of json formate or the binary data of zip,png
           @return dictionary of response
           @Exception URLError.
        '''
        logger = Logger.getLogger()
        #user define exception
        f = None
        try:
            logger.debug('>>>init request!')
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
            request.add_header('Content-Type',content_type)
            #add picture type expect img or the img of error screen
            if ext_type:
                request.add_header('Ext-Type',ext_type)
            #the content type of feedback from server
            request.add_header('Accept', 'application/json')
            #the length of data
            #request.add_header("Content-Length", str(len(postdata)))
            #the http request type GET POST PUT
            request.get_method = lambda: method
            urllib2.socket.setdefaulttimeout(10)
            logger.debug('>>>send request')
            f = urllib2.urlopen(request)
            logger.debug('>>>got request response')
            #headers = f.info()
            #json_feedback = f.read()
            return True

        except Exception,e:
            if hasattr(e, 'reason'):
                logger.debug('>>>Failed to reach a server.')
                logger.debug('%s %s' % ('Reason:',str(e.reason)))
            elif hasattr(e, 'code'):
                logger.debug('The server couldn\'t fulfill the request.')
                logger.debug('%s %s' % ('Error code:',str(e.code)))
            else:
                logger.debug('%s %s' % ('>>>sender exception:',str(e)))
            return False
        finally:
            if f != None:
                logger.debug('>>>socket release')
                urllib2.socket._closeActiveSockets()
                f.close()

class ResultSender(object):
    '''Class for uploading data to server.Support JSON and application/zip and image/png.
    '''
    __instance = None 
    __mutex = threading.Lock()

    def __init__(self):
        self.logger = Logger.getLogger()
        self.getUserAccount()
        #verify account and password
        self.token = self.getToken()
        if self.token is None:
            print 'Please check netwotk connection!' 
        assert self.token,'token is none'
        self.tid = 0
        self.queue = Queue.Queue(20)
        self.sessionId = str(uuid.uuid1())
        self.addTask(sessionStatus='sessionstart')

    def getUserAccount(self):
        '''Get user account info from sysconfig file'''
        _account = Parser.getUserAccountConfig()
        _server_url = _account.result_update_url
        _auth_url = _account.server_auth_url
        _username = _account.user
        _password = _account.password
        self._auth_url = _auth_url
        self._session_create_url = '%s%s%s%s' % (_server_url,'/test/','%s','/create')
        self._session_update_url = '%s%s%s%s' % (_server_url,'/test/','%s','/update')
        self._caseresult_create_url = '%s%s%s%s%s%s' % (_server_url,'/test/','%s','/case/','%s','/create')
        self._caseresult_update_url = '%s%s%s%s%s%s' % (_server_url,'/test/','%s','/case/','%s','/update')
        self._upload_file_url = '%s%s%s%s%s%s' % (_server_url,'/test/','%s','/case/','%s','/fileupload')
        self._auth_field = {'appid':'01','username':_username,'password':_password}

    def getToken(self):
        '''Get the value of session token from server side'''
        field = self._auth_field
        m = hashlib.md5()
        m.update(field['password'])
        pwd = m.hexdigest()
        #url = '%s?%s=%s&%s=%s&%s=%s' % (self._auth_url,'appid',field['appid'],'username',field['username'],'password',pwd)
        postdata = {'appid':field['appid'],'username':field['username'],'password':pwd}
        if True:
            f = None
            try:
                request = urllib2.Request(self._auth_url)
                request.add_header('Content-Type','application/json')
                request.add_header('Accept', 'application/json')
                request.add_data(minjson.write(postdata))
                request.get_method = lambda: 'POST'
                urllib2.socket.setdefaulttimeout(10)
                f = urllib2.urlopen(request)
                json_feedback = f.read()
                dic = eval(json_feedback)
                value = dic['results']['token']
                self.logger.debug('%s %s' % ('>>>Got token: ',str(value)))
                return value
            except Exception, e:
                if hasattr(e, 'reason'):
                    self.logger.debug('>>>Failed to reach a server.')
                    self.logger.debug('%s %s' % ('>>>Reason:',str(e.reason)))
                elif hasattr(e, 'code'):
                    self.logger.debug('The server couldn\'t fulfill the request.')
                    self.logger.debug('%s %s' % ('>>>Error code:',str(e.code)))
                else:
                    self.logger.debug('%s %s' % ('>>>get token exception:',str(e)))
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
            msg = self.parseMessage(msg_type=sessionStatus,session_id=self.sessionId) 
        elif info:
            if info[0]=='startTest':
                #creat case result id when start test
                self.tid += 1
            msg = self.parseMessage(msg_type='caseresult',session_id=self.sessionId,caseresult_id=self.tid,test_info=info,file_path=path)
        elif path:
            msg = self.parseMessage(msg_type='caseresult',session_id=self.sessionId,caseresult_id=self.tid,test_info=info,file_path=path)
 
        for task in msg:
            self.logger.debug(task['url'])
            #self.queue.put(task)
            #self.logger.debug('put over')
            try:
                self.queue.put(task,timeout=10)
                self.logger.debug('>>>put new task to queue')
                self.logger.debug('%s %s' % ('>>>current task queue size:',str(self.queue.qsize())))                
            except:
                self.queue.queue.clear()
                self.logger.debug('>>>task queue exception')
                self.logger.debug('>>>clear task queue')
                self.logger.debug('%s %s' % ('>>>current task queue size:',str(self.queue.qsize())))   

    #@staticmethod
    def parseMessage(self,msg_type=None,session_id=None,caseresult_id=None,test_info=None,file_path=None):
        '''Geneate request data functions'''
        logger = self.logger
        if msg_type == 'sessionstart':
            logger.debug('>>>>>>>>>>>>session start request')
            url = self._session_create_url % session_id
            sessionStarttime = TestBuilder.getBuilder().getProperty('starttime')
            deviceId = ''
            properties = {}
            try:
                deviceId = DeviceManager.getInstance().getDevice().getDeviceId()
                properties = DeviceManager.getInstance().getDevice().getDeviceInfo()
            except:
                deviceId = ''
                properties = {}
            postData = {'planname':'plan','starttime':sessionStarttime,'deviceid':deviceId,'deviceinfo':properties}
            contentType = 'application/json'
            method = 'POST'            
            return [{'url':url,'data':postData,'content_type':contentType,'method':method}]
        if msg_type == 'sessionstop':
            logger.debug('>>>>>>>>>>>>session end request')
            url = self._session_update_url % session_id
            sessionEndtime = time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))

            postData = {'endtime':sessionEndtime}
            contentType = 'application/json'
            method = 'POST'            
            return [{'url':url,'data':postData,'content_type':contentType,'method':method}]

        if msg_type == 'caseresult':
            #logger.debug('>>>>>>case update request<<<')
            sid = session_id
            tid = caseresult_id
            info = test_info
            path = file_path
            if info:
                if info[0] == 'startTest':
                    logger.debug('>>>>>>>>>>>>test case start request')
                    url = (self._caseresult_create_url) % (sid,tid)
                    caseName = info[1][1]._testMethodName
                    startTime = info[1][0].case_start_time
                    postData = {'casename':caseName,'starttime':startTime}
                    contentType = 'application/json'
                    method = 'POST'            
                    return [{'url':url,'data':postData,'content_type':contentType,'method':method}]
                elif info[0] == 'addSuccess':
                    logger.debug('>>>>>>>>>>>>test case pass request')
                    url = (self._caseresult_update_url) % (sid,tid)
                    _time = time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))
                    postData = {'result':'pass','time':_time,'traceinfo':'N/A'}
                    contentType = 'application/json'
                    method = 'POST'
                    return [{'url':url,'data':postData,'content_type':contentType,'method':method}]
                elif info[0] == 'addFailure':
                    logger.debug('>>>>>>>>>>>>test case failure request')
                    resultUrl = (self._caseresult_update_url) % (sid,tid)
                    resultTime = time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))
                    traceInfo = ResultSender._trace_to_string((info[1][2],info[1][1]))
                    resultPostData = {'result':'fail','time':resultTime,'traceinfo':traceInfo}
                    resultContentType = 'application/json'
                    resultMethod = 'POST'
                    resultRequest = {'url':resultUrl,'data':resultPostData,'content_type':resultContentType,'method':resultMethod}
                    #log file
                    url = (self._upload_file_url) % (sid,tid)
                    case_name = '%s.%s' %(type( info[1][1]).__name__,  info[1][1]._testMethodName)
                    case_starttime = info[1][0].case_start_time
                    testcase_result_folder = '%s-%s'%(case_name,case_starttime)
                    report_path =  os.path.join(TestBuilder.getBuilder().getWorkspace(),'report')
                    result_path = os.path.join(report_path,'%s-%s'% (TestBuilder.getBuilder().getProperty('product'),TestBuilder.getBuilder().getProperty('starttime')))     
                    dest = os.path.join(os.path.join(result_path,'fail',testcase_result_folder))
                    zipName = '%s.%s'%(testcase_result_folder,'zip')
                    logPath = os.path.join(dest,zipName)
                    logPostData = _openFile(logPath)
                    logContentType = 'application/zip'
                    logMethod = 'PUT'
                    failFileRequest = {'url':url,'data':logPostData,'content_type':logContentType,'method':logMethod}

                    rightFullPath = info[1][1].verifier.expectResult.getCurrentCheckPointParent()
                    dirs,rightFullName =  os.path.split(rightFullPath)
                    rightFullData = _openFile(rightFullPath)
                    expectFullRequest = {'url':url,'data':rightFullData,'content_type':'image/png','method':'PUT','exttype':'expect:'+rightFullName}
                    logger.debug('ready to send expect full snapshot with corrdinates')
                    logger.debug(rightFullPath)
                    return [resultRequest,failFileRequest,expectFullRequest]

                elif info[0] == 'addError':
                    logger.debug('>>>>>>>>>>>>test case error request')
                    resultUrl = (self._caseresult_update_url) % (sid,tid)
                    resultTime = time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))
                    traceInfo = ResultSender._trace_to_string((info[1][2],info[1][1]))
                    resultPostData = {'result':'error','time':resultTime,'traceinfo':traceInfo}
                    resultContentType = 'application/json'
                    resultMethod = 'POST'
                    resultRequest = {'url':resultUrl,'data':resultPostData,'content_type':resultContentType,'method':resultMethod}
                    return [resultRequest]
            elif file_path:
                logger.debug('>>>>>>>>>>>>upload current snapshot')
                sid = session_id
                tid = caseresult_id
                url = (self._upload_file_url) % (sid,tid)
                postData = _openFile(file_path)
                dirs,currentSnapshotName = os.path.split(file_path)
                contentType = 'image/png'
                method = 'PUT'
                return [{'url':url,'data':postData,'content_type':contentType,'method':method,'exttype':'current:'+currentSnapshotName}]

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
    '''Thread for sending http request from task queue'''
    def __init__(self,q):
        '''Init instance of Sender thread.'''
        threading.Thread.__init__(self)
        self.isStop = False
        self.task_queue = q
        self.logger = Logger.getLogger()

    def run(self):
        '''Thread work functions'''
        while not self.isStop:
            #if don't get tid from server. Can create thread for each request.
            try:
                self.logger.debug('%s %s' % ('>>>sender thread task queue size:',str(self.task_queue.qsize())))
                job = self.task_queue.get()
                self.logger.debug('>>>sender thread obtain a task from queue.')
                self.task_queue.task_done()
                success = SendUtils.request(job)
                if not success:
                    self.logger.debug('>>>sender thread upload result failed. Check network connection.')
                self.logger.debug('>>>sender thread finished a task.')
            except:
                #self.stop
                self.logger.debug('>>>Sender exception.')
            finally:
                pass

    def stop(self):
        '''Stop the thread'''
        self.isStop = True

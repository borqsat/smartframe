#!/usr/bin/env python  
#coding: utf-8

'''
Module provides the function to communicate with remote server.
@version: 1.0
@author: borqsat
@see: null
'''
import os,urllib2,glob,time,math,threading,thread,uuid
import ConfigParser
import json
import variables
from serialize import Serializer
from devicemanager import DeviceManager
from cStringIO import StringIO
import getpass
import hashlib
import base64
#from ps import Topics,emit

#reference_url = 'http://ats.borqs.com/smartserver/login.html'

def _time():
    return time.strftime(variables.TIME_STAMP_FORMAT, time.localtime(time.time()))


class Authentication(object):
    @staticmethod
    def auth():
        print '\nwhen enable --upload there requires accountname/password.\n'
        account_name = raw_input('Enter account name:\n')
        password = base64.b64encode(getpass.getpass('Enter password:\n'))
        auth_url = None
        token = None
        #validate token if validation failed. get a new token.
        #TODO: add function to verify the token from server
        if os.path.exists(variables.TOKEN_CONFIG_PATH):
            return
        #read server config 
        server_info = ConfigParser.ConfigParser()
        server_info.read(variables.SERVER_CONFIG_PATH)
        auth_url = None
        try:
            auth_url = server_info.get('server','authentication_url')
            if not auth_url:
                raise
        except Exception,e:
            print 'invalid config file %s\n' % variables.SERVER_CONFIG_PATH
            #abort due to read error. sys.exit(1)

        #do auth
        md = hashlib.md5()
        md.update(base64.b64decode(password))
        pwd_encode = md.hexdigest()
        postdata = {'appid':'01','username':account_name,'password':pwd_encode}
        response = None
        try:
            request = urllib2.Request(auth_url)
            request.add_header('Content-Type','application/json')
            request.add_header('Accept', 'application/json')
            request.add_data(json.dumps(postdata))
            request.get_method = lambda: 'POST'
            response = urllib2.urlopen(request,timeout=10)
            json_feedback = response.read()
            dic = eval(json_feedback)
            if 'errors' in dic.keys():
                raise Exception('account name or password incorrect')
            token = dic['results']['token']
        except urllib2.URLError, ue:
            print ue
            sys.exit(1)
            
        except urllib2.HTTPError, he:
            print he
            sys.exit(1)

        except Exception, e:
            if hasattr(e, 'reason'):
                print 'Failed to reach a server.'
                print '%s %s' % ('Reason:',str(e.reason))
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print '%s %s' % ('Error code:',str(e.code))
            else:
                print '%s %s' % ('Get token failed:',str(e))
            sys.exit(1)      
        finally:
            if response != None:
                response.close()

        cf = ConfigParser.ConfigParser()
        cf.read(variables.TOKEN_CONFIG_PATH)
        if not cf.has_section('account'):
            cf.add_section('account')
        cf.set('account','account',account_name)
        cf.set('account','password',password)
        cf.set('account','token',token)
        with open(variables.TOKEN_CONFIG_PATH,'wb') as f:
            cf.write(f)
class ResultUploader(object):
    """
    Singleton class for uploading result
    """

    # lock object
    __lockObj = thread.allocate_lock()

    # the unique instance
    __instance = None

    def __new__(cls, *args, **kargs):
        return cls.getInstance(cls, *args, **kargs)

    def __init__(self):
        self._sid = None
        self._sender = None
        self._urls = {}
        self._getConfigFromFile(variables.SERVER_CONFIG_PATH)
        self._token = self._getTokenFromFile(variables.TOKEN_CONFIG_PATH)

    def _getConfigFromFile(self,path):
        assert os.path.exists(path),'%s file not found!' % path
        url = None
        try:
            server_info = ConfigParser.ConfigParser()
            server_info.read(path)
            url = server_info.get('server','upload_url')
        except:
            raise Exception('invalid config file %s\n' % path)
        #NOW sid,tid created on server
        self._urls['session_create_url'] = '%s%s%s%s' % (url,'/test/','%s','/create')
        self._urls['session_update_url'] = '%s%s%s%s' % (url,'/test/','%s','/update')
        self._urls['caseresult_create_url'] = '%s%s%s%s%s%s' % (url,'/test/','%s','/case/','%s','/create')
        self._urls['caseresult_update_url'] = '%s%s%s%s%s%s' % (url,'/test/','%s','/case/','%s','/update')
        self._urls['upload_file_url'] = '%s%s%s%s%s%s' % (url,'/test/','%s','/case/','%s','/fileupload')

    def _getTokenFromFile(self,path):
        assert os.path.exists(path),'%s file not found!' % path
        token = None
        try:
            account_info = ConfigParser.ConfigParser()
            account_info.read(path)
            token = account_info.get('account','token')
        except:
            raise Exception('invalid config file %s\n' % path)
        return token

    @classmethod
    def getInstance(cls, *args, **kargs):
        """
        Static method to have a reference to **THE UNIQUE** instance
        """
        # Critical section start
        cls.__lockObj.acquire()
        try:
            if cls.__instance is None:
                # (Some exception may be thrown...)
                # Initialize **the unique** instance
                cls.__instance = object.__new__(cls, *args, **kargs)
                cls.__instance.__init__()
                #setattr(cls.__instance,)
        finally:
            # Exit from critical section whatever happens
            cls.__lockObj.release()
        # Critical section end
        return cls.__instance

    def upload(self,path):
        if not self._sender:
            print '>>>>>>send_therad: _sender is None. first sender create'
            self._sender = Sender(workspace=path, urls=self._urls,token=self._token)
            self._sender.setDaemon(True)
            self._sender.start()
        if not self._sender.isAlive():
            print '>>>>>>send_therad: _sender is not None. but not alive. create it again'
            self._sender = Sender(workspace=path, urls=self._urls,token=self._token)
            self._sender.setDaemon(True)
            self._sender.start()


class Sender(threading.Thread):
    '''
    Thread for uploading result to remote server
    '''
    def __init__(self,workspace,urls,token):
        '''
        Init the instance of Sender.
        '''
        threading.Thread.__init__(self)
        self._work_space = workspace
        self._urls = urls
        self._token = token
        self._stop = False
        self._handled = False
        #self._block = False

    def run(self):
        '''
        The work method.
        '''
        while not self._stop:
            #if don't get tid from server. Can create thread for each request.
            try:
                print '>>>>>>send_thread: begin'
                #STEP1 session create:
                self.session_id = None
                session_path = os.path.join(self._work_space,'.session')
                #if .session exists. then the session has been created on server
                #if .session not exists. then the session will be created on server
                if os.path.exists(session_path) and not self.session_id:
                    obj = Serializer.unserialize(session_path)
                    self.session_id = obj['sid']
                    print 'session id--------------\n'
                    print self.session_id
                else:
                    print '>>>>>>send_thread: first create session on server'
                    #init session id on local
                    self.session_id = str(uuid.uuid1())
                    datas = {'token':self._token,'planname':'plan','starttime':time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))}
                    datas.update(DeviceManager.getDevice().getDeviceProperties())
                    request = {'method':'POST',
                           'url':self._urls['session_create_url'] % self.session_id,
                           'Content-Type':'application/json',
                           'Accept':'application/json',
                           'data':datas
                    }
                    print request
                    if RequestUtils.send(request):
                        datas.update({'sid':self.session_id})
                        Serializer.serialize(file_path=session_path, data=datas)
                    else:
                        print '<<<<<<<<<<send_thread: session request failed'
                        continue
                
                if self.upload(): break
                else: continue
                #while not self._block:
                #    if not self.upload():
                #        return
                #    else:
                #        continue

            except Exception,e:
                print e
                print 'exception when uploading'
            finally:
                pass
            print '>>>>>>send_thread: ---------------------EXIT-----------------------'

    def stop(self):
        '''
        Stop the thread.
        '''
        self._stop = True

    def block(self):
        '''
        Stop the thread.
        '''
        self._block = True

    def upload(self):
        request = None
        result = []
        ws = os.path.join(self._work_space,'all')
        for d in os.listdir(ws):
            bd = os.path.join(ws,d)
            if os.path.isdir(bd): result.append(bd)
        def callback(fs):
            p,f = os.path.split(fs)
            return int(time.mktime(time.strptime(f.split('@')[-1], variables.TIME_STAMP_FORMAT)))
        path = min(result, key=callback)
        target = os.path.basename(path)
        print 'target--------------------------------------------------------------------\n'
        print target
        case_name, case_start_time = target.split(variables.FILE_NAME_SEPARATOR)
        result_file_path = os.path.join(path,variables.RESULT_FILE_NAME)
        tid_file_path = os.path.join(path,variables.TID_FILE_NAME)
        if os.path.exists(result_file_path):
            print '>>>>>>send_thread: find result file begin to update test result'
            #SWITCH TO update test case result on server
            datas = Serializer.unserialize(file_path=result_file_path)
            tid = datas.pop('tid')
            datas.update({'token':self._token,'casename':case_name,'starttime':case_start_time})
            print 'result update TID:'
            print str(tid)
            if datas['result'] == 'pass':
                print 'ready to send PASS result request'
                request = {'method':'POST',
                           'url':self._urls['caseresult_update_url']%(self.session_id,str(tid)),
                           'Content-Type':'application/json',
                           'Accept':'application/json',
                           'data':datas
                           }
                print request
                if RequestUtils.send(request):
                    print 'pass result upload over'
                else:
                    print '<<<<<<<<<<send_thread: equest failed'
                    return False

            if datas['result'] == 'fail':
                print 'FAIL'
                request = {'method':'POST',
                           'url':self._urls['caseresult_update_url'] % (self.session_id,str(tid)),
                           'Content-Type':'application/json',
                           'Accept':'application/json',
                           'data':datas
                           }
                print request
                if RequestUtils.send(request):
                    print 'fail result upload over'
                else:
                    print '<<<<<<<<<<send_thread: equest failed'
                    return False

                #files = [(os.stat(i).st_mtime, i) for i in glob.glob(os.path.join(path,'%s%s'%('*',variables.IMAGE_SUFFIX)))]
                #files.sort()
                #snaps = [i[1] for i in files]
                #print '>>>>>>send_thread: waiting for uploading'
                #print snaps
                #print '>>>>>>send_thread:waiting for uploading'
                #for f in snaps:
                #    if RequestUtils.send():
                #        print 'upload snapshots %s over' % str(f)
                #    else:
                #        print '<<<<<<<<<<send_thread: equest failed'
                #        self.stop()
                #        return

            if datas['result'] == 'error':
                request = {'method':'POST',
                           'url':self._urls['caseresult_update_url']%(self.session_id,str(tid)),
                           'Content-Type':'application/json',
                           'Accept':'application/json',
                           'data':datas
                           }
                print request
                if RequestUtils.send(request):
                    print 'pass result upload over'
                else:
                    print '<<<<<<<<<<send_thread: equest failed'
                    return False
            #tid = tid + 1
            import shutil
            print '>>>>>>send_thread: upload success delete the orgin folder DELETING-------'
            #print path
            a = shutil.rmtree(path)
            return True
        elif os.path.exists(tid_file_path):
            print 'create test case request>>>>>>>>>>>>>>>>>'
            datas = Serializer.unserialize(file_path=tid_file_path)
            print datas['tid']
            request = {'method':'POST',
                       'url':self._urls['caseresult_create_url'] % (self.session_id,datas['tid']),
                       'Content-Type':'application/json',
                       'Accept':'application/json',
                       'data':{'token':self._token,'casename':case_name,'starttime':case_start_time}}
            print request
            if RequestUtils.send(request):
                print '>>>>>>send_thread: case create request success'
                #if create request OK. stop sender thread.
                self.stop()
                return True
            else:
                print '<<<<<<<<<<send_thread: request failed'
                return False
        else:
            return True

# Retry decorator with exponential backoff
def retry(tries, delay=1, backoff=2):
  '''Retries a function or method until it returns True.
 
  delay sets the initial delay, and backoff sets how much the delay should
  lengthen after each failure. backoff must be greater than 1, or else it
  isn't really a backoff. tries must be at least 0, and delay greater than
  0.'''

  if backoff <= 1:
    raise ValueError("backoff must be greater than 1")

  tries = math.floor(tries)
  if tries < 0:
    raise ValueError("tries must be 0 or greater")

  if delay <= 0:
    raise ValueError("delay must be greater than 0")

  def deco_retry(f):
    def f_retry(*args, **kwargs):
      mtries, mdelay = tries, delay # make mutable

      rv = f(*args, **kwargs) # first attempt
      while mtries > 0:
        if rv == True or type(rv) == str or type(rv) == dict: # Done on success ..
          return rv

        mtries -= 1      # consume an attempt
        time.sleep(mdelay) # wait...
        mdelay *= backoff  # make future wait longer

        rv = f(*args, **kwargs) # Try again

      return False # Ran out of tries :-(

    return f_retry # true decorator -> decorated function
  return deco_retry  # @retry(arg[, ...]) -> true decorator

class RealtimeCapturer(object):
    '''
    Class for uploading content to server.
    '''
    def __init__(self,dm,path):
        self._stop = False
        self._device = dm.getDevice()
    
    def capture(self):
        snapshot = self._device.getCurrentSnapshot(path)
        Message(topic=TOPICS.SNAPSHOT,data=snapshot)()

    def run(self):
        while not self._stop:
            self.capture()

class RequestUtils(object):
    '''
    Uploading content to server. start when enable "--upload" argument and network available, server available.
    '''
    debugid = 1
    @staticmethod
    #@retry(3)
    def send1(kwargs):
        '''
        sends a Request.
        Parameters:
        method - method for the new Request object. (GET POST DELETE PUT)
        url - URL for the new Request object.
        params - (optional) Dictionary or bytes to be sent in the query string for the Request.
        data - (optional) Dictionary, bytes, or file-like object to send in the body of the Request.
        headers - (optional) Dictionary of HTTP Headers to send with the Request.
        cookies - (optional) Dict or CookieJar object to send with the Request.
        files - (optional) Dictionary of name: file-like-objects (or {name: (filename, fileobj)}) for multipart encoding upload.
        timeout - (optional) Float describing the timeout of the request.
        @rtype: boolean
        @return: true if server return OK. flase if server return failed.
        '''
        response = None
        ret = None
        try:
            request = urllib2.Request(kwargs['url'])
            request.add_header('Content-Type',kwargs['Content-Type'])
            request.add_header('Accept', kwargs['Accept'])
            request.add_data(json.dumps(kwargs['data']))
            request.get_method = lambda: kwargs['method']
            response = urllib2.urlopen(request,timeout=10)
            json_feedback = response.read()
            ret = eval(json_feedback)
            print ret
            if 'errors' in ret.keys():
                raise Exception('Errors from server!')

        except urllib2.URLError, ue:
            print ue
            return False
            
        except urllib2.HTTPError, he:
            print he
            return False

        except Exception, e:
            if hasattr(e, 'reason'):
                print 'Failed to reach a server.'
                print '%s %s' % ('Reason:',str(e.reason))
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print '%s %s' % ('Error code:',str(e.code))
            else:
                print '%s %s' % ('Get token failed:',str(e))
                print 'remote server network unavaiable'
            return False

        finally:
            if response != None:
                response.close()
        return ret

    i = 1
    @staticmethod
    @retry(3)
    def send(kwargs):
        print '>>>>>>send_thread sneding:%s'%str(RequestUtils.i)
        if RequestUtils.i < 3:
            RequestUtils.i = RequestUtils.i + 1
            print '>>>>>>send_thread retry: failed. retry...'
            return False
        else:
            print '>>>>>>send_thread retry over: OK'
            return True

#TODO used to monitor uploading status
class Progress(object):
    def __init__(self):
        self._seen = 0.0

    def update(self, total, size, name):
        self._seen += size
        pct = (self._seen / total) * 100.0
        print '%s progress: %.2f' % (name, pct)

#uploading progress status if necessary
class file_with_callback(file):
    def __init__(self, path, mode, callback, *args):
        file.__init__(self, path, mode)
        self.seek(0, os.SEEK_END)
        self._total = self.tell()
        self.seek(0)
        self._callback = callback
        self._args = args

    def __len__(self):
        return self._total

    def read(self, size):
        data = file.read(self, size)
        self._callback(self._total, len(data), *self._args)
        return data

#path = 'large_file.txt'
#progress = Progress()
#stream = file_with_callback(path, 'rb', progress.update, path)
#req = urllib2.Request(url, stream)
#res = urllib2.urlopen(req)
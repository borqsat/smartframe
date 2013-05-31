#!/usr/bin/env python  
#coding: utf-8

'''
Module provides the function to communicate with remote server.
@version: 1.0
@author: borqsat
@see: null
'''

import json
reference_url = 'http://ats.borqs.com/smartserver/login.html'

class NetworkMonitor(object):
    '''
    Class for monitor network status.
    '''
    def getConnectivityStatus(self,reference_url):
        '''
        check if the network is avaiable.
        @rtype: boolean
        @return: true is avaiable, false if unavaiable
        '''

    def notify(self,status):
        #emit(Topics.Network,status)
        pass

class RequestFile(object):
    def __init__(self,file_path):
        self.f = file_path

    def getData(self):
        '''
        Return the instance of Message
        rtype: {}
        rvalue: {}
        '''
        pass

    def getFileName(self):
        '''
        Return the request file name
        rtype: string
        rvalue: the request file name
        '''
        pass

    def delete(self):
        '''
        Delete the local request file if uploading success
        '''
        try:
            os.remove(self.f)
        except:
            pass

class PackageScaner(object):
    '''
    Class to maintan the request files package.
    '''
    def __init__(self,root_path):
        self._root_path = root_path
        self._is_session_request = True
        #self._session_start_path = os.path.join(root_path,SESSION_START_REQ)
        #self._session_end_path = os.path.join(root_path,SESSION_END_REQ)

    def getLatestRequest(self):
        '''
        Get The request file need to be uploaded.
        rtype: RequestFile
        rvalue: Return instance of RequestFile
        '''
        pass

class ResultUploader(object):
    '''
    Thread to upload files.
    '''
    def __init__(self, pkg_scaner,options):
        super(Uploader,self).__init__()
        self._session_token = None
        self._sid = None
        self._tid = None
        self.retry = False
        self.block = False
        self.scaner = pkg_scaner
        self.setDaemon(True)

    def restart(self):
        '''
        Restart thread work.
        '''
        self.block = False

    def stop(self):
        '''
        Idle the thread.
        rtype: RequestFile
        rvalue: Return instance of RequestFile
        '''
        self.block = True

    def doUpload(self,data):
        '''
        Use RequestUtils to do the http upload
        '''
        pass
        #RequestUtils.send(data)

    def run(self):
        while not self.block:
            req = self.scaner.getLatestRequest()
            data = req.getData()
            doUpload(data)
            pass

class RealtimeCapturer(object):
    '''
    Class for uploading content to server.
    '''
    def __init__(self):
        self.stop = False
    
    def capture(self):
        snapshot = None
        Message(topic=TOPICS.SNAPSHOT,data=snapshot)()

    def run(self):
        while not self.stop:
            self.capture()


class RequestUtils(object):
    '''
    Uploading content to server. start when enable "--upload" argument and network available, server available.
    '''
    def send(self, method, url, retry_count=3, **kwargs):
        '''
        sends a Request.
        Parameters:
        method - method for the new Request object. (GET POST DELETE)
        url - URL for the new Request object.
        params - (optional) Dictionary or bytes to be sent in the query string for the Request.
        data - (optional) Dictionary, bytes, or file-like object to send in the body of the Request.
        headers - (optional) Dictionary of HTTP Headers to send with the Request.
        cookies - (optional) Dict or CookieJar object to send with the Request.
        files - (optional) Dictionary of name: file-like-objects (or {name: (filename, fileobj)}) for multipart encoding upload.
        auth - (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        timeout - (optional) Float describing the timeout of the request.
        allow_redirects - (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.
        proxies - (optional) Dictionary mapping protocol to the URL of the proxy.
        verify - (optional) if True, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
        stream - (optional) if False, the response content will be immediately downloaded.
        cert - (optional) if String, path to ssl client cert file (.pem). If Tuple, (cert, key) pair.
        @rtype: dictionary
        @return: {}
        '''
        #res = requests.request(method,url,kwargs)
        #data = json.load(res)
        data = {}
        return data

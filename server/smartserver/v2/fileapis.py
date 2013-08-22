from gevent import monkey
monkey.patch_all()

from bottle import request, response, Bottle
from gevent.pywsgi import WSGIServer

from .impl.test import *
from .config import WEB_HOST, WEB_PORT  # import db configuration

appfs = Bottle()

@appfs.route('/log/<fid>', method='GET')
def doGetCaseResultLog(fid):
    """
    URL:/log/<fid>
    TYPE:http/GET

    Get test case log file

    @type  fid: string
    @param fid: the id of case result
    @type data:JSON
    @param data:{'token':(string)value}
    @rtype: JSON
    @return:ok
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    data = getTestCaseLog(fid)
    if isinstance(data, type({})):
        return data
    else:
        filename = 'log-%s.zip' % fid
        response.set_header('Content-Type', 'application/x-download')
        response.set_header('Content-Disposition', 'attachment; filename=' + filename)
        return data

@appfs.route('/snap/<fid>', method='GET')
def doGetCaseResultLog(fid):
    """
    URL:/snap/<fid>
    TYPE:http/GET

    Get test case snap file
    @type  fid: string
    @param tid: the file id of case snap
    @type data:JSON
    @param data:{'token':(string)value}
    @rtype: JSON
    @return:ok
            error-{'errors':{'code':value,'msg':(string)info}}
    """
    data = getTestCaseSnap(fid)
    if isinstance(data, type({})):
        return data
    else:
        response.set_header('Content-Type', 'image/png')
        return data


def main():
    port = WEB_PORT
    host = WEB_HOST
    print 'FileSystem Serving on %s:%d...' % (host, port)
    WSGIServer(("", port), appfs).serve_forever()


if __name__ == '__main__':
    main()

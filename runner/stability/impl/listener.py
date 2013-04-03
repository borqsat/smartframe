'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

from libs.pubsub import pub
from builder import TestBuilder
from resulthandler import ResultHandler

def collectResult(func):
    '''Decorator of collecting test results method'''
    def wrap(*args, **argkw):
        func(*args, **argkw)
        if True:
            content = (func.__name__,args)
            pub.sendMessage('collectresult',info=content)
        return func
    return wrap

def onTopicResult(info=None,path=None,sessionStatus=None):
    '''sort test session's result.
    Arguments:
    info -- the test case instance
    path: the file path need to be uploaded
    sessionStatus: the session status
    '''
    ResultHandler.handle(info,path,sessionStatus)
		
def onTopicGui(guiMsg):
    '''Topic for updating UI'''
    pass

def onTopicMemoryTrack():
    '''Topic for memory monitor'''
    pass

#mapper = {'collectresult':onTopicResult,
#            'gui':onTopicGui,
#            'memorytrack':onTopicMemoryTrack}

#print 'init pubsub listener begin:'
handler = ResultHandler()
pub.subscribe(handler.handle,'collectresult')
#pub.subscribe(reconnect,'reconnecttopic')


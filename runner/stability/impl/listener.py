from pubsub import pub
from stability.util.log import Logger
from builder import TestBuilder
from resulthandler import ResultHandler

def collectResult(func):
    def wrap(*args, **argkw):
        func(*args, **argkw)
        if True:
            content = (func.__name__,args)
            #print 'deco:::'
            #print func.__name__
            #print self,test,err
            #print args[0].case_start_time
            #print 'pub caseresult>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            pub.sendMessage('collectresult',info=content)
        return func
    return wrap

def collectSnapshot(func):
    def wrap(*args, **argkw):
        func(*args, **argkw)
        if True:
            snapshot_path = args[1]
            #print 'deco:::'
            #print func.__name__
            #print self,test,err
            #print args[0].case_start_time
            #print '<<<<<<<<<<<<<<<collectsnapshot?????????????????????'
            pub.sendMessage('collectresult',path=snapshot_path)
        return func
    return wrap

def onTopicResult(info=None,path=None,sessionStatus=None):
    '''sort test session's result.
    Keyword arguments:
    kwags -- should specify the data structure of argument.
    types: sessioncreate,caseresult
    info: (methodname,test,error) (methodname,test) info[0]:addStart,addStop,addSuccess,addFailure,addError
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
#print 'init pubsub listener over:'
#for (k,v) in mapper.items():
#    print '-'+str(k)
#    pub.subscribe(v,k)


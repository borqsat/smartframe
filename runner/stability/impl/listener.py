from pubsub import pub
from stability.util.log import Logger
from builder import TestBuilder
from resulthandler import ResultHandler

def onTopicResult(info=None,path=None):
    '''sort test session's result.
    Keyword arguments:
    kwags -- should specify the data structure of argument.
    types: sessioncreate,caseresult
    info: (methodname,test,error) (methodname,test) info[0]:addStart,addStop,addSuccess,addFailure,addError
    '''
    ResultHandler.handle(info,path)
		
def onTopicGui(guiMsg):
    '''Topic for updating UI'''
    pass

def onTopicMemoryTrack():
    '''Topic for memory monitor'''
    pass

mapper = {'collectresult':onTopicResult,
            'gui':onTopicGui,
            'memorytrack':onTopicMemoryTrack}

print 'init pubsub listener:'
for (k,v) in mapper.items():
    print '-'+str(k)
    pub.subscribe(v,k)

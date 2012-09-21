import os
from configparser import ConfigParser

class BuildHelper(object):
    TEST_DIR_NAME = 'testcase'
    CASE_DIR_NAME = 'cases'
    RESULT_DIR_NAME = 'result'
    PLAN_DIR_NAME = 'plan'
    RESULT_RIGHT_DIR_NAME = 'right'
    RESULT_ALL_DIR_NAME = 'all'
    RESULT_FAIL_DIR_NAME = 'fail'
    RESULT_ERROR_DIR_NAME = 'error'
    RESULT_PASS_DIR_NAME = 'pass'
    LOG_DIR_NAME = 'log'
    SESSION_DIR_NAME = 'session'
     
    def __init__(self,path):
        self.root = path

    def getTests(self):
        planDir = self.getPlanDir()
        print planDir
        tests = ConfigParser.readTests(planDir)
        return tests
    
    def getDefaultWorkspace(self):
        return os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
    def getWorkspace(self):
        return os.path.abspath(self.root)
        
    def getPlanDir(self):
        return  os.path.join(self.root,'plan')
      
    def getResultDir(self):
        #print 'getResultDir()>>>>>>\n'
        #print os.path.join(self.root,'result')
        return os.path.join(self.root,'result')
       
    def getResultRightDir(self):
        return os.path.join(self.getResultDir(),'right')

    def getResultAllDir(self):
        return os.path.join(self.getResultDir(),'all') 
     
    def getResultFailDir(self):
        return os.path.join(self.getResultDir(),'fail')         

    def getResultErrorDir(self):
        return os.path.join(self.getResultDir(),'error')
 
    def getPlanDir(self):
        return os.path.join(self.getWorkspace(),'plan')
      
    def getLogDir(self):
        return os.path.join(self.getWorkspace(),'log')
      
    def getLogDir(cls,test):
        return os.path.join(self.getWorkspace(),'session')
       
    def validateStructure(self):
        #if os.path.exists(self.rootPath): 
        pass


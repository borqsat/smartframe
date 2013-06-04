'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''

import logging,time,os,threading,sys
import logging.handlers

#File Level
FILE_LOG_LEVEL="DEBUG"

#Console Level
CONSOLE_LOG_LEVEL="INFO"

#logger levels
LEVELS={"CRITICAL" :50,
        "ERROR" : 40,
        "WARNING" : 30,
        "INFO" : 20,
        "DEBUG" : 10,
        "NOTSET" :0,
       }  

class Logger:
    _instance=None
    _mutex=threading.Lock()

    def __init__(self, level="DEBUG"):
        '''Generate root logger'''
        self._logger = logging.getLogger("SmartRunner")
        self._logger.setLevel(LEVELS[level])
        self._formatter = logging.Formatter("[%(asctime)s] - %(levelname)s : %(message)s",'%Y-%m-%d %H:%M:%S')
        self._formatterc = logging.Formatter("%(message)s")
        self.add_file_logger()
        self.add_console_logger()

    def add_file_logger(self, logFile="./log/test.log", file_level="DEBUG"):
        '''Generate file writer [RotatingFileHandler]'''
        logFolder = 'log'
        if not os.path.exists(logFolder):
            os.makedirs(logFolder)
        if not os.path.exists(logFile):
            open(logFile,'w')
            
        fh = logging.handlers.RotatingFileHandler(logFile,mode='a',maxBytes=1024*1024*1,
                                                   backupCount=100,encoding="utf-8")
        fh.setLevel(LEVELS[file_level])
        fh.setFormatter(self._formatter)
        self._logger.addHandler(fh)

    def add_console_logger(self, console_level="INFO"):
        '''Generate console writer [StreamHandler]'''
        ch = logging.StreamHandler()
        ch.setLevel(LEVELS[console_level])
        ch.setFormatter(self._formatterc)
        self._logger.addHandler(ch)

    @staticmethod
    def getLogger(level="DEBUG"):
        if(Logger._instance==None):
            Logger._mutex.acquire()
            if(Logger._instance==None):
                Logger._instance=Logger(level)
            else:
                pass
            Logger._mutex.release()
        else:
            pass
        return Logger._instance

    def debug(self,msg):
        if msg is not None:
            self._logger.debug(msg)

    def info(self,msg):
        if msg is not None:
            self._logger.info(msg)

    def warning(self,msg):
        if msg is not None:
            self._logger.warning(msg)

    def error(self,msg):
        if msg is not None:
            self._logger.error(msg)

    def critical(self,msg):
        if msg is not None:
            self._logger.critical(msg)

#global logger instance
logger = Logger.getLogger()
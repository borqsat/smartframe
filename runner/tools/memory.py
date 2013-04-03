#!/usr/bin/env python  
 
import commands
import os
import sys
import time
import string
 
CMD_STAT = 'adb shell stat -f '


class Memory(object):
  
    def memory(self):
        self.extSys_argvs()
        res = commands.getoutput('adb root')
        print res
        time.sleep(2)
        self.getDataSize()
        data = self.getInputSize(self.percent)
        self.inputData(data)
        print 'SUCCESS!'

    def getDataSize(self):
        result = commands.getoutput(CMD_STAT + self.path)
        index_total = result.find('Total:',0)
        index_free = result.find('Free:', 0)
        index_available = result.find('Available:', 0)
        self.total = int(result[index_total+7:index_free].strip())*4/1024
        self.free = int(result[index_free+6:index_available].strip())*4/1024
        self.used = self.total - self.free
        print '%s Total:%iM' % (self.path, self.total)
        print 'Used:%iM' % (self.used)
        print 'Free:%iM' % (self.free)

    def getInputSize(self, percent):
        per = 0.01*int(percent)
        input_size = self.total*per - self.used
        if input_size <= 0:
            print 'Input size %iM is not bigger than 0, no need to fill!'%(input_size)
            sys.exit()
        print 'Input %iM data to %s.'%(input_size, self.path)
        return input_size

    def inputData(self, size):
        filehandler = open('test.txt','w')
        filehandler.seek(int(1024*1024*size))
        filehandler.write('\x00')  
        filehandler.close()  
        commands.getoutput('adb push test.txt %s'%(self.path))

    #check commands and get percent data
    def extSys_argvs(self):
        strArg = ''.join(sys.argv)
        if strArg.find('-p') == -1 or strArg.find('-d')== -1:
	    self.showUsage()
            sys.exit()
        else:
            argPIndex = sys.argv.index('-p')
            argDIndex = sys.argv.index('-d')
            if argPIndex != 1:
		self.showUsage()
                sys.exit()
            else:
                if argPIndex == len(sys.argv)-3:
		    self.showUsage()
		    sys.exit()
                elif sys.argv[argPIndex + 1].isdigit() == False:
                    print 'Please using digit for percent!'
                    sys.exit()
            self.percent = sys.argv[argPIndex + 1]
            if argDIndex != 3:
		self.showUsage()
                sys.exit()
            elif argDIndex == len(sys.argv)-1:
		    self.showUsage()
		    sys.exit()
            self.path = sys.argv[argDIndex + 1]
    
    def showUsage(cls):
        print 'Usage:'
        print 'python memory.py [-p percent][-d path_dir]'
        print '-p percent : percent that you want to fill memory'
        print '-d path_dir: which path you want to fill, /data or /mnt/sdcard'
        print '                 e.g.'
        print '                 python memory.py -p 90 -d /data'

if (__name__ == '__main__'):
    memory = Memory()
    memory.memory()
    

#!/usr/bin/python
# -*- coding:utf-8 -*- 
import threading
import logging
import datetime
import os
import platform

DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3
CRITICAL = 4

class LoggingRecord(object):
    '''the log file will automatically be divided by date,such as 2012-12-14.log,2012-12-15.log, '''
    __output_dict = {
                      DEBUG:(logging.Logger.debug,"debug"),
                      INFO:(logging.Logger.info,"info"),
                      WARNING:(logging.Logger.warn,"warning"),
                      ERROR:(logging.Logger.error,"error"),
                      CRITICAL:(logging.Logger.critical,"critical")
                      }
    def __init__(self,record_name):
        self.__today = None
        self.__file_handler = None
        self.__lock = threading.Lock()
        self.__log_dir = None
        self.__logger = logging.getLogger(record_name)
        #self.__logger.propagate = False

    def initialize(self,logdir,level,output_to_console):
        if not os.path.isdir(logdir):
            try:
                os.mkdir(logdir)
            except OSError,e:
                print str(e)
                return False
        self.__log_dir = logdir
        if platform.system() != "Windows" and not os.access(self.__log_dir,os.R_OK|os.W_OK|os.X_OK):
            print "the directory is not accessible:",logdir
            return False
        self.__logger.setLevel(level)
        if output_to_console:
            stream_handler = logging.StreamHandler()
            self.__logger.addHandler(stream_handler)
        else:
            self.__logger.propagate = False
        return True

    def clear(self):
        if self.__file_handler:
            self.__logger.removeHandler(self.__file_handler)
            self.__file_handler.close()
            self.__file_handler = None

    def log_str(self,level,infos):
        self.__lock.acquire()
        now = datetime.datetime.now()
        today = now.date()
        if today != self.__today:
            if self.__file_handler:
                self.__logger.removeHandler(self.__file_handler)
                self.__file_handler.close()
            filename = today.isoformat() + ".log"
            filename = self.__log_dir + "/" + filename
            self.__today = today
            self.__file_handler = logging.FileHandler(filename)
            self.__logger.addHandler(self.__file_handler)
        method,level_name = self.__output_dict[level]
        import thread
        thread_id = thread.get_ident()
        output_str = "[%s],[%d],[%s],%s" % (now.isoformat(),thread_id,level_name,infos)
        method(self.__logger,output_str)
        self.__lock.release()

logging_recorders = {}

def add_recorder(record_name,path,level,output_to_console=False):
    global logging_recorders
    if logging_recorders.has_key(record_name):
        print "log recorder already exists",record_name
        return False
    level_dict = {"default":logging.NOTSET,"debug":logging.DEBUG,"info":logging.INFO,\
                "warnning":logging.WARNING,"error":logging.ERROR,"critical":logging.CRITICAL}
    if not level_dict.has_key(level):
        print "invalid level:",level
        return False
    level = level_dict[level]
    recorder = LoggingRecord(record_name)
    if not recorder.initialize(path,level,output_to_console):
        return False
    logging_recorders[record_name] = recorder
    return True

def add_multiple_recorders(names,base_dir,level,output_to_console=False):
    count = 0
    for item in names:
        path = "%s/%s" % (base_dir,item)
        if add_recorder(item,path,level,output_to_console):
            count += 1
    return count

def remove_all():
    for key in logging_recorders.keys():
        recorder = logging_recorders[key]
        recorder.clear()
    logging_recorders.clear()
        

def get_recorder(record_name):
    global logging_recorders
    if logging_recorders.has_key(record_name):
        return logging_recorders[record_name]
    return None

def output(record_name,level,text):
    recorder = get_recorder(record_name)
    if not recorder:
        return False
    recorder.log_str(level,text)
    return True

def debug(record_name,text):
    output(record_name,DEBUG,text)
def info(record_name,text):
    output(record_name,INFO,text)
def warn(record_name,text):
    output(record_name,WARNING,text)
def error(record_name,text):
    output(record_name,ERROR,text)
def critical(record_name,text):
    output(record_name,CRITICAL,text)

#just for testing
if __name__ == '__main__':
    record_names = ("logic","protocol",)
    count = add_multiple_recorders(record_names,"./log","debug",True)
    print "success to add %d records" % count
    for record_name in record_names:
        for i in range(0,10,1):
            debug(record_name,"[%s:I'm here as always]"%record_name)
            info(record_name,"[%s:I'm here as always]"%record_name)
            warn(record_name,"[%s:I'm here as always]"%record_name)
            error(record_name,"[%s:I'm here as always]"%record_name)
            critical(record_name,"[%s:I'm here as always]"%record_name)
        raw_input("press")
    print "remove all recorders"
    raw_input("press")
    remove_all()

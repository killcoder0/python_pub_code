#!/usr/bin/python
# -*- coding:utf-8 -*- 

import xylogging

LOGGER_NAME_LOGIC = "logic"
LOGGER_NAME_PROTOCOL = "protocol"
LOGGER_NAME_PERFORMANCE = "performance"

LOG_TYPE_SYS = "system"
LOG_TYPE_LOGIC = "logic"
LOG_TYPE_MGMT = "mgmt"

def LogicLog(id,operation,result,info):
    try:
        return LOGGER_NAME_LOGIC,"[%s],[%s],[%s],[%s],[%s]" % (LOG_TYPE_LOGIC,str(id),operation,result,info)
    except:
        return LOGGER_NAME_LOGIC,"except:LogicLog"

def SystemLog(posinfo,apiname,errinfo):
    try:
        filename,lineno = (posinfo[0],posinfo[1])
        return LOGGER_NAME_LOGIC,"[%s],[%s],[%s],[%s],[%s]" % (LOG_TYPE_SYS,filename,str(lineno),apiname,errinfo)
    except:
        return LOGGER_NAME_LOGIC,"except:SystemLog"

def MgmtLog(sourceip,url,response):
    try:
        return LOGGER_NAME_LOGIC,"[%s],[%s],[%s],[%s]" % (LOG_TYPE_MGMT,sourceip,url,response)
    except:
        return LOGGER_NAME_LOGIC,"except:MgmtLog"

def CommLog(src_end,dst_end,request_url,request_body,response): 
    try:
        if request_body:
            request_content = request_body
        else:
            request_content = ""       
        if response:
            response_content = response
        else:
            response_content = ""
        double_line =  "\n===================================\n"
        single_line = "\n-----------------------------------\n"
        return LOGGER_NAME_PROTOCOL,"%s[%s],[%s],[%s],%s%s%s%s%s" % (single_line,src_end,dst_end,request_url,single_line,
                                                          request_content,single_line,response_content,double_line)
    except:
        return LOGGER_NAME_PROTOCOL,"except:CommLog"

def StatisticEventLog(actionid,operation,action_time,addition_info=""):
    try:
        if not addition_info:
            attach_info = ""
        else:
            attach_info = addition_info
        return LOGGER_NAME_PERFORMANCE,"[Event],[%s],[%s],[%s],[%s]" % (str(actionid),operation,str(action_time),attach_info)
    except:
        return LOGGER_NAME_PERFORMANCE,"except:StatisticEventLog"

def FuncProfileLog(FuncName,posinfo,time_cost,addition_info=""):
    try:
        if not addition_info:
            attach_info = ""
        else:
            attach_info = addition_info
        filename,lineno = (posinfo[0],posinfo[1])
        posinfo = "%s:%d"%(filename,lineno)
        return LOGGER_NAME_PERFORMANCE,"[Function],[%s],[%s],[%s],[%s]" % (FuncName,posinfo,str(time_cost),attach_info)
    except:
        return LOGGER_NAME_PERFORMANCE,"except:FuncProfileLog"

def debug(args):
    try:
        xylogging.debug(args[0],args[1])
    except Exception,e:
        print str(e)

def info(args):
    try:
        xylogging.info(args[0],args[1])
    except Exception,e:
        print str(e)

def warn(args):
    try:
        xylogging.warn(args[0],args[1])
    except Exception,e:
        print str(e)

def error(args):
    try:
        xylogging.error(args[0],args[1])
    except Exception,e:
        print str(e)

def critical(args):
    try:
        xylogging.critical(args[0],args[1])
    except Exception,e:
        print str(e)


def report_standard_http_response(response,attach_info,action_name):
    if not response or response.error:
        critical(LogicLog("None",action_name,"http_error",attach_info))
    else:
        import json
        resp = json.loads(response.body)
        if resp["result"] == "ok":
            info(LogicLog("None",action_name,"ok",attach_info))
        else:
            info_msg = "[attach_info:%s][err_info:%s]" % (attach_info,resp["err"]["info"])
            error(LogicLog("None","AddChannelToChunkServer","fail",info_msg))

#code below is just for testing
def main():
    import sys
    sys.path.append("../pub")

    #prepare
    record_names = (LOGGER_NAME_LOGIC,LOGGER_NAME_PROTOCOL,LOGGER_NAME_PERFORMANCE,)
    count = xylogging.add_multiple_recorders(record_names,"./log","debug",True)
    print "success to add %d records" % count
    if count != len(record_names):
        xylogging.remove_all()
        return
    #logic logger
    debug(LogicLog(12345,"transcode","ok","no definition to video info"))
    info(MgmtLog("192.168.16.35","http://master.com:8888/get_task",'{"result":"fail","err":"unknown"}'))
    warn(MgmtLog("192.168.16.34","http://master.com:8888/get_task",'{"result":"ok"}'))
    import common.utils as utils
    error(SystemLog(utils.get_cur_info(),"bomb","break,bomb"))
    critical(LogicLog(23456,"SaveVBaseInfo","fail","unknown"))
    critical(LogicLog(0,"ConnectToRedis","fail","network truble"))
    #communication logger
    debug(CommLog("local","192.168.16.188:8080","/addTask",'{"seq":228283,"site":"yk","priority":3}','{"success":true}'))
    #performance
    info(StatisticEventLog("SpiderAddTask-1","start",1382779822.794,None))
    error(StatisticEventLog("SpiderAddTask-1","end",1382780355.481,None))
    import common.utils
    info(FuncProfileLog("Print",common.utils.get_cur_info(),0.001))
    raw_input("press")


if __name__ == "__main__":
    main()
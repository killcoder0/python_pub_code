#!/usr/bin/python
# -*- coding:utf-8 -*-

#set path
import sys
sys.path.append("../")

def init_taskmgr(queue_name_list,processor_class_list,algorithm):
    import queue_mgr
    return queue_mgr.initialize(queue_name_list,processor_class_list,algorithm)

def init_engine(domain_conn_limit,default_conn_limit=10,timeout=20):
    #initialize the http client engine
    import http_client_engine
    if not http_client_engine.initialize(domain_conn_limit,default_conn_limit):
        return False
    import etc
    etc.request_timeout = timeout
    return True

def start_spider(entry_map,interval,finish_callback):
    import controller
    if not controller.initialize(finish_callback):
        return False
    return controller.fire(entry_map,interval)

if __name__ == "__main__":
    pass
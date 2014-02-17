#!/usr/bin/python
# -*- coding:utf-8 -*-

import tornado.ioloop
import time
from xlog import logginghelper

STATE_WAITING = "waiting"
STATE_PROCESSING = "processing"
STATE_FINISHED = "finished"
 
class Controller(object):
    def __init__(self,callback_finish):
        #state
        self.__state = STATE_WAITING
        #interval
        self.__interval = 0
        #finish callback function
        self.__finish_cbfunc = callback_finish

    def get_state(self):
        return '{"state":"%s"}' % self.__state

    def set_state(self,state):
        self.__state = state
        if state == STATE_FINISHED and self.__finish_cbfunc:
            self.__finish_cbfunc()
    
    def _post_delay_cycle(self):
        instance = tornado.ioloop.IOLoop.instance()
        deadline = time.time() + self.__interval
        instance.add_timeout(deadline,self.fire)
        self.__state = STATE_WAITING
    
    def fire(self,entry_map,interval):
        self.__interval = interval
        self.__state = STATE_PROCESSING
        import id_mgr
        act_id = id_mgr.get_new_id()
        id_mgr.set_id("SpiderID",act_id)
        logginghelper.info(logginghelper.StatisticEventLog(str(act_id),"Spider",str(time.time()),"Start"))
        import req_gen
        import net_task
        for url,processor_class in entry_map:
            req = req_gen.make_request(url)
            job = net_task.make_job(req,None,None)
            cb_obj = processor_class(job)
            job.execute(cb_obj.handle_response)
        return True

_controller = None

def initialize(callback_finish=None):
    global _controller
    if _controller:
        return False
    _controller = Controller(callback_finish)
    return True

def fire(entry_map,interval):
    return _controller.fire(entry_map,interval)

def set_state(state):
    _controller.set_state(state)

def get_status():
    return _controller.get_state()

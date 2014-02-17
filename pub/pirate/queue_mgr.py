#!/usr/bin/python
# -*- coding:utf-8 -*-

import task_queue

class QueueMgr(object):
    def __init__(self):
        self.__task_queues = []

    def initialize(self,queue_name_list,queue_processor_list,algorithm):
        if self.__task_queues:
            return False
        queue_count = len(queue_name_list)
        if queue_count != len(queue_processor_list):
            return False
        for index in range(0,queue_count):
            queue_name = queue_name_list[index]
            if queue_name in queue_name[index+1:]:
                return False
            processor_class = queue_processor_list[index]
            queue_obj = task_queue.TaskQueue(processor_class)
            self.__task_queues.append((queue_name,queue_obj))
        self.__algorithm = algorithm
        return True

    def get_next_queue(self,queue_name):
        if not queue_name:
            return self.__task_queues[0]
        current = 0
        for queue_obj in self.__task_queues:
            current += 1
            if queue_obj[0] == queue_name:
                break
        if current == len(self.__task_queues):
            return None
        return self.__task_queues[current]

    def get_queue(self,queue_name):
        if not queue_name:
            return self.__task_queues[0]
        for name,queue_obj in self.__task_queues:
            if queue_name == name:
                return (name,queue_obj)
        return (None,None)

    def get_count(self,queue_name=None):
        if not queue_name:
            count = 0
            for item in self.__task_queues:
                queue_obj = item[1]
                count += queue_obj.get_count(None)
            return count
        for name,queue_obj in self.__task_queues:
            if name == queue_name:
                return queue_obj.get_count(None)
        return -1

    def signal(self,domain):
        import http_client_engine
        engine = http_client_engine.get_engine()
        free_count = engine.get_free_conn(domain)
        if self.__algorithm == "BFS":
            queues = self.__task_queues
        else:
            queues = reversed(self.__task_queues)
        for item in queues: 
            while free_count > 0:
                if not item[1].signal(domain):
                    break
                free_count -= 1
        #check if there is no pending request for this manager
        if engine.get_pending_count() == 0 and self.get_count() == 0:
            import controller
            controller.set_state(controller.STATE_FINISHED)

    def get_queue_status(self):
        result = {}
        for queue_name,queue_obj in self.__task_queues:
            result[queue_name] = queue_obj.get_count(None)
        return result


_queue_mgr = QueueMgr()

def get_mgr():
    return _queue_mgr

def initialize(queue_name_list,queue_processor_list,algorithm):
    return _queue_mgr.initialize(queue_name_list,queue_processor_list,algorithm)
    
from xlog import logginghelper

class TaskQueue(object):
    def __init__(self,cb_class):
        self._domain_task_queue = {}
        self._cb_class = cb_class
        self._delay = {}
    
    def set_delay(self,domain,has_delay=True):
        self._delay[domain] = has_delay

    def get_delay(self,domain):
        return self._delay.has_key(domain) and self._delay[domain]

    def get_count(self,domain):
        if not domain:
            count = 0
            for key in self._domain_task_queue.keys():
                if self.get_delay(domain):
                    count += 1
                count += len(self._domain_task_queue[key])
            return count
        count = len(self._domain_task_queue[domain])
        if self.get_delay(domain):
            count += 1
        return count

    def put(self,job):
        if not self._domain_task_queue.has_key(job.domain):
            task_q = [job,]
            self._domain_task_queue[job.domain] = task_q
        else:
            task_q = self._domain_task_queue[job.domain]
            task_q.append(job)


    #sub class could invoke this first
    def signal(self,domain):
        if not self._domain_task_queue.has_key(domain):
            return False
        if self.get_delay(domain):
            return False
        task_q = self._domain_task_queue[domain]
        if len(task_q) == 0:
            return False
        job = task_q.pop(0)
        cb_obj = self._cb_class(job)
        if not job.execute(cb_obj.handle_response):
            logginghelper.error(logginghelper.LogicLog("None","AddRequest","fail",job.request.url))
            return False
        return True

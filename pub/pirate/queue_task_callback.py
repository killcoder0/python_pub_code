from xlog import logginghelper

class CallbackWrapper(object):
    '''base class for other job's callback'''
    def __init__(self,job):
        self._job = job

    def handle_response(self,response):
        domain_set = {self._job.domain}
        if response.error:
            if self._job.retry_times != -1 and self._job.failure_times == self._job.retry_times:
                err = response.error
                info = "%d+%s+%s" % (err.code,str(err.message),self._job.request.url)
                logginghelper.error(logginghelper.LogicLog("None","Request","fail",info))
                return (False,domain_set)
            self._job.execute(self.handle_response)
            self._job.failure_times += 1
            return (False,None)
        return (True,domain_set)

def signal_domain(callback):
    def _wrapper(self,response):
        domain_set = callback(self,response)
        if not domain_set:
            return
        import queue_mgr
        for domain in domain_set:
            queue_mgr.get_mgr().signal(domain)
    return _wrapper

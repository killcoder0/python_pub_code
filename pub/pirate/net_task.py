import urlparse

class Job(object):
    def __init__(self,request,domain,cur_queue_name,context,engine,retry_times):
        self.request = request
        self.domain = domain
        self.in_queue = cur_queue_name
        self.context = context
        self.retry_times = retry_times
        self.failure_times = 0
        if not engine:
            import http_client_engine
            self.engine = http_client_engine.get_engine()
        else:
            self.engine = engine

    def execute(self,callback):
        return self.engine.fetch(self.request,callback)


def make_job(request,queue_name,context,engine=None,retry_times=10):
    result = urlparse.urlparse(request.url)
    if not result.hostname:
        return None
    return Job(request,result.hostname,queue_name,context,engine,retry_times)

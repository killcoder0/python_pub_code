#!/usr/bin/python
# -*- coding:utf-8 -*-

import tornado.httpclient
import tornado.curl_httpclient
import urlparse

class HTTPClientEngine(object):
    '''this class has such features: connection persistent,connection selector'''

    def __init__(self,site_conn_limit,default_limit):
        #the request count which is in network
        self.__penging_count = {}
        #the client info to speicified domain
        self.__client_mgr = {}
        #concurrent connection count limit if which is not specified
        self.__conn_default_limit = default_limit
        #concurrent connection count limit to specified website
        if not site_conn_limit or not isinstance(site_conn_limit,dict):
            self.__conn_limit = {}
        else:
            self.__conn_limit = site_conn_limit

    def on_response(self,response):
        url = response.request.url
        domain = urlparse.urlparse(url).hostname
        client = self.__client_mgr[domain]
        client.pending_count -= 1
        if client.pending_count < 0:
            pass
    
    class EngineClient(object):
        def __init__(self,client,pending_count=0):
            self.client = client
            self.pending_count = pending_count

    class CallbackWrapper(object):
        def __init__(self,engine,cbFunc):
            self.__engine = engine
            self.__callback = cbFunc

        def callback(self,response):
            self.__engine.on_response(response)
            self.__callback(response)

    def fetch(self,request,cbFunc):
        #form such as www.baidu.com,google
        domain = None
        try:
            result = urlparse.urlparse(request.url)
            if not result.hostname or not result.scheme:
                return False
            domain = result.hostname
        except Exception:
            return False
        if self.__client_mgr.has_key(domain):
            client = self.__client_mgr[domain]
        else:
            if self.__conn_limit.has_key(domain):
                max_cli = self.__conn_limit[domain]
            else:
                max_cli = self.__conn_default_limit
            curl_client = tornado.curl_httpclient.CurlAsyncHTTPClient(max_clients=max_cli)
            client = self.EngineClient(curl_client)
            self.__client_mgr[domain] = client
        cb_obj = self.CallbackWrapper(self,cbFunc)
        client.client.fetch(request,cb_obj.callback)
        client.pending_count += 1
        return True

    def set_conn_limit(self,domain,count):
        if self.__client_mgr.has_key(domain):
            return False
        self.__conn_limit[domain] = count
        return True

    def get_conn_limit(self,domain):
        if not domain or not self.__conn_limit.has_key(domain):
            return self.__conn_default_limit
        return self.__conn_limit[domain]

    def get_pending_count(self,domain=None):
        if not domain:
            count = 0
            for key in self.__client_mgr.keys():
                count += self.__client_mgr[key].pending_count
            return count
        if not self.__client_mgr.has_key(domain):
            return 0
        return self.__client_mgr[domain].pending_count

    def get_pending_statistics(self):
        result = {}
        for domain in self.__client_mgr.keys():
            result[domain] = self.__client_mgr[domain].pending_count
        return result

    def get_free_conn(self,domain):
        return self.get_conn_limit(domain) - self.get_pending_count(domain)

_engine = None

def initialize(site_conn_limit=None,default_limit=10):
    global _engine
    if _engine:
        return False
    _engine = HTTPClientEngine(site_conn_limit,default_limit)
    return True

def get_engine():
    return _engine

########################################################################################
#below coding is just for testing
def test_on_response(response):
    engine = get_engine()
    print "current request count in pending:"," www.baidu.com:",engine.get_pending_count("www.baidu.com",),"www.qq.com:",engine.get_pending_count("www.qq.com",)
    print "Connection:",response.headers["Connection"]

if __name__ == "__main__":
    initialize()
    this_engine = get_engine()
    import req_gen
    for i in range(0,30):
        req = req_gen.make_request("http://www.baidu.com/",no_keep_alive=False)
        this_engine.fetch(req,test_on_response)
        req = req_gen.make_request("http://www.qq.com/",no_keep_alive=False)
        this_engine.fetch(req,test_on_response)
        print "www.baidu.com:",this_engine.get_pending_count("www.baidu.com",),"www.qq.com:",this_engine.get_pending_count("www.qq.com",)
    import tornado.ioloop
    tornado.ioloop.IOLoop.instance().start()



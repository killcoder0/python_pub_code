import cookie_storage
import tornado.httputil
import tornado.httpclient
import urlparse
import copy
import urlparse

def get_domain(url):
    result = urlparse.urlparse(url)
    return result.netloc.lower()

def create_cookie_header(cookie):
    if not cookie or len(cookie) == 0:
        return tornado.httputil.HTTPHeaders()
    return tornado.httputil.HTTPHeaders({"Cookie":cookie})

def _create_request(cookie_stg,url,method,headers,body,connect_timeout=10,request_timeout=10):
    cookie = cookie_stg.gen_header_cookies(url) 
    req_headers = create_cookie_header(cookie)
    if headers:
        for key in headers.keys():
            req_headers.add(key,headers[key])
    return tornado.httpclient.HTTPRequest(url,method,req_headers,body,None,None,connect_timeout,request_timeout,follow_redirects=False)

#class HandlerFilter(object):
#    def __init__(self,handler,filter):
#        self.__handler = handler
#        self.__filter = filter
#    def handle_response(self,response,seq):
#        self.__filter(response)
#        self.__handler(response,seq)


class Session(object):
    def __init__(self):
        self._cookie_stg = cookie_storage.CookieStg()

    def _filter_response(self,response):
        if not response:
            return
        headers = response.headers
        cookie_list = headers.get_list("set-cookie")
        domain = get_domain(response.request.url)
        if cookie_list:
            for line in cookie_list:
                self._cookie_stg.add_cookie_from_http_header(line,domain)

    def fetch(self,url,method,headers,body,connect_timeout=10,request_timeout=10):
        req = _create_request(self._cookie_stg,url,method,headers,body,connect_timeout,request_timeout)
        client = tornado.httpclient.HTTPClient()
        try:
            response = client.fetch(req)
        except Exception,e:
            response = e.response
        if not response:
            return None
        self._filter_response(response)
        if response.code in (301, 302, 303, 307):
            new_url = urlparse.urljoin(url,response.headers["Location"])
            return self.fetch(new_url,method,headers,body,connect_timeout,request_timeout)
        return response

    def send_form(self,action,method,data_map,add_header_=None,connect_timeout=10,request_timeout=10):
        if not add_header_:
            add_header = {}
        else:
            import copy
            add_header = copy.copy(add_header_)
        add_header["content-type"] = "application/x-www-form-urlencoded"
        try:
            import urllib
            args = urllib.urlencode(data_map)
        except Exception,e:
            return None
        if method in ("GET","get"):
            url = "%s?%s" % (action,args)
        else:
            url = action
        return self.fetch(url,method,add_header,args,connect_timeout,request_timeout)

    def report(self):
        self._cookie_stg.print_cookie()

class AsyncSession(Session):
    def __init__(self):
        Session.__init__(self)
    
    class ResponseFilter(object):
        def __init__(self,handler,filter):
            self.__handler = handler
            self.__filter = filter
        def handle_response(self,response):
            if not response.error:
                self.__filter(response)
                if response.code in (301, 302, 303, 307):
                    new_url = urlparse.urljoin(response.request.url,response.headers["Location"])
                    new_req = copy.copy(response.request)
                    new_req.url = new_url
                    client = tornado.httpclient.AsyncHTTPClient()
                    client.fetch(new_req,self.handle_response)
                    return
            self.__handler(response)

    def fetch(self,url,method,headers,body,response_handler,connect_timeout=10,request_timeout=10):
        req = _create_request(self._cookie_stg,url,method,headers,body,connect_timeout,request_timeout)
        client = tornado.httpclient.AsyncHTTPClient()
        handler = self.ResponseFilter(response_handler,self._filter_response)
        client.fetch(req,handler.handle_response)
        return True

    def send_form(self,action,method,data_map,reponse_handler,add_header=None,connect_timeout=10,request_timeout=10):
        if not add_header:
            add_header = {}
        add_header["content-type"] = "application/x-www-form-urlencoded"
        try:
            import urllib
            args = urllib.urlencode(data_map)
        except Exception,e:
            return False
        if method in ("GET","get"):
            url = "%s?%s" % (action,args)
        else:
            url = action
        self.fetch(url,method,add_header,args,reponse_handler,connect_timeout,request_timeout)
        return True
 

import cookie_storage
import tornado.httputil

REQUEST_TYPE_GET = 0
REQUEST_TYPE_TXT_POST = 1
REQUEST_TYPE_FORM_POST = 2

def create_cookie_header(cookie):
    if not cookie or len(cookie) == 0:
        return None
    return tornado.httputil.HTTPHeaders({"Cookie":cookie})

def create_form_header(cookie):
    header = tornado.httputil.HTTPHeaders(
                  {"content-type":"application/x-www-form-urlencoded"})
    if not cookie or len(cookie) == 0:
        return header
    header.add("Cookie",cookie)
    return header

class HandlerFilter(object):
    def __init__(self,handler,filter):
        self.__handler = handler
        self.__filter = filter
    def handle_response(self,response,seq):
        self.__filter(response)
        self.__handler(response,seq)

class Session(object):
    def __init__(self):
	    self.__cookie_stg = cookie_storage.CookieStg()

    def filter_response(self,response):
        header = response.headers
        cookie_list = header.get_list("set-cookie")
        if cookie_list:
            for line in cookie_list:
                self.__cookie_stg.add_cookie_from_http_header(line)

    def create_header_and_method(self,url,request_type):
        #add cookie to request header
        cookie = self.__cookie_stg.gen_header_cookies(url)
        if request_type == REQUEST_TYPE_GET:
            header = create_cookie_header(cookie)
            method = "GET"
        elif request_type == REQUEST_TYPE_TXT_POST:
            header = create_cookie_header(cookie)
            method = "POST"
        elif request_type == REQUEST_TYPE_FORM_POST:
            header = create_form_header(cookie)
            method = "POST"
        else:
            return (None,None)
        return (header,method)

    def send_data(self,handler,url,request_type,body,connect_timeout=1,request_timeout=10):
        header,method = self.create_header_and_method(url,request_type)
        if (header,method) == (None,None):
            return -1
        filter = HandlerFilter(handler,self.filter_response)
        return AsyncCallMgr.post_request_job(filter.handle_response,url,method,
                                      header,body,connect_timeout,request_timeout)

    def get(self,handler,url,sync=False):
        if not sync:
            return self.send_data(handler,url,REQUEST_TYPE_GET,None)
        return self.sync_send_data(url,REQUEST_TYPE_GET,None)

    def sync_get(self,url):
        return self.get(None,url,True)


    def post_text(self,handler,url,body=None,sync=False):
        if not sync:
            return self.send_data(handler,url,REQUEST_TYPE_TXT_POST,body)
        return self.sync_send_data(url,REQUEST_TYPE_TXT_POST,body)

    def sync_post_text(self,url,body=None):
        return self.post_text(None,url,body,True)

    def post_form(self,handler,url,form_data,sync=False):
        body = ""
        for key in form_data.keys():
            item = "%s=%s" % (key,form_data[key])
            if len(body) != 0:
                body += "&"
            body += item
        if not sync:
            return self.send_data(handler,url,REQUEST_TYPE_FORM_POST,body)
        return self.sync_send_data(url,REQUEST_TYPE_FORM,body)

    def sync_post_form(self,url,form_data):
        return self.post_form(None,url,form_data,True)

    def sync_send_data(self,url,request_type,_body,_connect_timeout=1,_request_timeout=10):
        _header,_method = self.create_header_and_method(url,request_type)
        if (_header,_method) == (None,None):
            return None
        http_client = tornado.httpclient.HTTPClient()
        try:
            request = tornado.httpclient.HTTPRequest(url,connect_timeout=_connect_timeout,
                                             request_timeout=_request_timeout,
                                             headers=_header,body=_body,
                                             method=_method,
                                             max_redirects = -1)
            response = http_client.fetch(request)
        except httpclient.HTTPError, e:
            print "sync http call error:",e
            return None
        return response

    def report(self):
       self.__cookie_stg.print_cookie()

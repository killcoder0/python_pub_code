#!/usr/bin/python
# -*- coding:utf-8 -*- 

import httplib

class ServerResponse(object):
    def __init__(self,code,headers,body):
        self.code = code
        self.headers = headers
        self.body = body

    def pack_http_response_buf(self):
        status = httplib.responses.get(self.code)
        if not status:
            status = "Unknown"
        segs = []
        segs.append("HTTP/1.1 %u %s" % (self.code,status))
        for key,value in self.headers.iteritems():
            segs.append("%s:%s"%(key,value))
        if self.body == None:
            body = status
        else:
            body = str(self.body)
        segs.append("Content-Length:%d" % len(body))
        message = "%s\r\n\r\n%s" % ("\r\n".join(segs),body)
        return message

def render_to_response(body,code=200,headers={}):
    return ServerResponse(code,headers,body)

def pack_response(code):
    resp = render_to_response("",code)
    return resp.pack_http_response_buf()

def login_required(auth_func):
    def _deco(handler):
        def __deco(request):
            if auth_func(request):
                return handler(request)
            return render_to_response("",401,{"WWW-Authenticate":'Basic realm="insert realm"'})
        return __deco
    return _deco

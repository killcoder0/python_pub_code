#!/usr/bin/python
# -*- coding:utf-8 -*- 

import httplib
import re
import tornado.httpserver
import tornado.ioloop
import xhttp_utils
from pub.common import error

class XRequestHandler(object):
    ''' Callback handler to dispatch and handle request'''

    def __init__(self,url_match_list):
        self.__router = url_match_list

    def handle_request(self,request):
        #if self.__router.has_key(request.path):
        #    handler = self.__router[request.path]
        #else:
        #    handler = None
        request_handler = None
        for re_str,handler in self.__router:
            if re.match(re_str,request.path):
                request_handler = handler
                break
        if not request_handler:
            resp = xhttp_utils.render_to_response(None,404)
        else:
            try:
                resp = request_handler(request)
            except Exception,e:
                resp = xhttp_utils.render_to_response(None,500)
        message = resp.pack_http_response_buf()
        request.write(message)
        request.finish()

def pack_response(code,headers={},body=""):
    status = httplib.responses.get(code)
    if not status:
        status = "Unknown"
    segs = []
    segs.append("HTTP/1.1 %u %s" % (code,status))
    for key,value in headers.iteritems():
        segs.append("%s:%s"%(key,value))
    body = str(body)
    segs.append("Content-Length:%d" % len(body))
    message = "%s\r\n\r\n%s" % ("\r\n".join(segs),body)
    return message

def start(ports,url_map=None,_no_keep_alive=True):
    request_handler = XRequestHandler(url_map)
    if not isinstance(ports,tuple):
        ports = (ports,)
    for port in ports:
        http_server = tornado.httpserver.HTTPServer(request_handler.handle_request,no_keep_alive=_no_keep_alive)
        http_server.listen(int(port))
    tornado.ioloop.IOLoop.instance().start()
    return True

def stop():
    tornado.ioloop.IOLoop.instance().stop()
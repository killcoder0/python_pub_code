#!/usr/bin/python
# -*- coding:utf-8 -*- 

import tornado.httpserver
import tornado.ioloop
from common import error
import urls

class XRequestHandler(object):
    ''' Callback handler to dispatch and handle request'''

    def __init__(self,url_map):
        self.__router = url_map

    def handle_request(self,request):
        if self.__router.has_key(request.path):
            handler = self.__router[request.path]
        else:
            handler = None
        if not handler:
            body = error.pack_errinfo_json(error.ERROR_HTTP_URL_NOT_SUPPORTED)
        else:
            body = handler(request)
        message = "HTTP/1.1 200 OK\r\nContent-Length:%d\r\n\r\n%s" % (len(body),body)
        request.write(message)
        request.finish()

def start(port,url_map=None):
    request_handler = XRequestHandler(url_map)
    http_server = tornado.httpserver.HTTPServer(request_handler.handle_request,no_keep_alive=True)
    http_server.listen(int(port))
    tornado.ioloop.IOLoop.instance().start()
    print "thread to quit:Main Thread"
    return True
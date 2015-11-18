#!/usr/bin/python
# -*- coding:utf-8 -*- 

import httplib
import re
import tornado.httpserver
import tornado.ioloop
from pub.xhttp import xhttp_utils
from pub.xhttp import tornado_helper
from pub.common import error

class XRequestHandler(object):
    ''' Callback handler to dispatch and handle request'''

    def __init__(self,url_match_list):
        self.__router = url_match_list

    def reset_router(self,url_match_list):
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
                print str(e)
                resp = xhttp_utils.render_to_response(None,500)
        message = resp.pack_http_response_buf()
        request.write(message)
        request.finish()

request_handler = None

def start(ports,url_map=None,_no_keep_alive=True):
    global request_handler
    request_handler = XRequestHandler(url_map)
    if not isinstance(ports,tuple):
        ports = (ports,)
    for port in ports:
        http_server = tornado.httpserver.HTTPServer(request_handler.handle_request,no_keep_alive=_no_keep_alive)
        http_server.listen(int(port))
    tornado.ioloop.IOLoop.instance().start()
    return True

def stop():
    def _stop():
        tornado.ioloop.IOLoop.instance().stop()
        global request_handler
        request_handler = None
        #make sure the listening socket is closed,avoid the other restarting prcoessing is reuse it
        tornado.ioloop.IOLoop.instance().close(True)
    #tornado.ioloop.IOLoop.instance().add_callback(_stop)
    tornado_helper.add_timeout(0,_stop)

def reset_url_map(url_match_list):
    request_handler.reset_router(url_match_list)

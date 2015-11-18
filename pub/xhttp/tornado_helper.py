import tornado.ioloop
import functools
import datetime

def add_timeout(delay_seconds,callback,*args,**keywords):
    delta = datetime.timedelta(seconds=delay_seconds)
    timeout_cb = functools.partial(callback,*args,**keywords)
    return tornado.ioloop.IOLoop.instance().add_timeout(delta,timeout_cb)

def remove_timeout(timeout):
    tornado.ioloop.IOLoop.instance().remove_timeout(timeout)
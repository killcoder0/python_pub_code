#!/usr/bin/python
# -*- coding:utf-8 -*- 
import tornado.httpclient
import json


def post_txt(request_url,data):
    client = tornado.httpclient.HTTPClient()
    try:
        request = tornado.httpclient.HTTPRequest(url=request_url,method="POST",body=data)
        response = client.fetch(request)
        return response
    except tornado.httpclient.HTTPError,e: 
        return None

def post_json(request_url,json_data):
    try:
        data = json.dumps(json_data)
        return post_txt(request_url,data)
    except:
        return None

def get(request_url):
    client = tornado.httpclient.HTTPClient()
    try:
        request = tornado.httpclient.HTTPRequest(url=request_url,method="GET")
        response = client.fetch(request)
        return response
    except tornado.httpclient.HTTPError,e:
        return None



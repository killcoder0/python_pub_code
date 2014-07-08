#!/usr/bin/python
# -*- coding:utf-8 -*-  

import json

#protocal exception
ERROR_HTTP_URL_NOT_SUPPORTED = ("00.00","url not supported")
ERROR_HTTP_METHOD_NOT_SUPPORTED = ("00.01","http method not supported")

#businiess base protocal exception
ERROR_JSON_SYNTAX_ERROR = ("01.00","syntax error to json")

#business logic error
ERROR_PARAM_NO_PRIMARY_KEY = ("02.00","primary key missing")
ERROR_PARAM_INVALID_VALUE = ("02.01","invalid value to key")
ERROR_PARAM_NO_KEY      =   ("02.02","no such key")
ERROR_PARAM_ARG_MISSING = ("02.03","parameter missing")

ERROR_PARAM_INVALID_PARAMETER = ("10.00","invalid parameter parameter")
ERROR_PARAM_INVALID_KEY      =   ("10.01","invalid field")
ERROR_PARAM_KEY_ALREADY_EXISTS = ("10.02","specified key already exists")
ERROR_PARAM_KEY_NOT_EXIST      = ("10.03","specified key not exists")
ERROR_PARAM_UNIQUE_ID_REPEATED = ("10.04","unique identification repeated")

ERROR_SYSTEM_DATABASE = ("20.00","database throwed exception")

#http 
ERROR_HTTP_REQUEST_INVALID = ("30.00","invalid http request")
ERROR_HTTP_REQUEST_TIMEOUT = ("30.01","http request time out")
ERROR_HTTP_RESPONSE_INVALID = ("30.02","invalid http response")
ERROR_HTTP_RESPONSE_TIMEOUT = ("30.03","http response time out")

ERROR_INTERNAL_SERVER_ERROR = ("90.00","server internal error")
ERROR_INTERNAL_UNKNOWN_ERROR = ("90.91","unknown error")


def pack_errinfo_json(error,detail=None):
    result = {"result":"fail","err":{}}
    result["err"]["code"] = error[0]
    result["err"]["info"] = error[1]
    if detail:
        result["err"]["parameter"] = detail
    result = json.dumps(result)
    return result

def match(code,error_tuple):
    return code == error_tuple[0]

def pack_ok_json():
    return '{"result":"ok"}'

if __name__ == "__main__":
    print pack_errinfo_json(ERROR_INTERNAL_SERVER_ERROR,"shit")
    raw_input()
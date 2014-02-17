import json
import tornado.httpclient
import etc

AGENT_PC_CHROME = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36"
AGENT_MOBILE_ANDROID = "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
AGENT_MOBILE_IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
AGENT_MOBILE_IPAD = "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"

OS_TYPE_WINDOWS = 0
OS_TYPE_ANDROID = 1
OS_TYPE_IPHONE = 2
OS_TYPE_IPAD = 3

def make_request(url,data=None,ostype=OS_TYPE_WINDOWS,no_keep_alive=False):
    agent_list = (AGENT_PC_CHROME,AGENT_MOBILE_ANDROID,AGENT_MOBILE_IPHONE,AGENT_MOBILE_IPAD,)
    agent = agent_list[ostype]
    if no_keep_alive:
        conn_seg = "Close"
    else:
        conn_seg = "Keep-Alive"
    headers = {"Connection":conn_seg,"User-Agent":agent}
    if not data:
        method = 'GET'
    else:
        method = 'POST'
    timeout = etc.request_timeout
    return tornado.httpclient.HTTPRequest(url,method,headers,data,connect_timeout=timeout,request_timeout=timeout)

def make_json_request(url,json_map,ostype=OS_TYPE_WINDOWS):
    data = json.dumps(json_map)
    return make_request(url,data,ostype)


if __name__ == "__main__":
    client = tornado.httpclient.HTTPClient()
    #GET
    req = make_request("http://www.baidu.com/")
    resp = client.fetch(req)
    print resp.body
    raw_input("press")
    #POST
    req = make_request("http://music.baidu.com/search",data="os=ios&key=sail")
    resp = client.fetch(req)
    print resp.body
    raw_input("press")
    #POST JSON
    req = make_json_request("http://music.baidu.com/search",{"os":"ios","key":"sail"})
    resp = client.fetch(req)
    print resp.body
    raw_input("press")

import urlparse

class PathCookies(object):
    def __init__(self,domain,path):
        self.domain = domain
        self.path = path
        self.cookies = {}

class CookieStg(object):
    def __init__(self):
        # domain -->  PathCookies list
        self.__domains = {}

    def add_cookie_pair(self,domain,path,pair):
        domain = domain.lower()
        path = path.lower()
        if not self.__domains.has_key(domain):
            self.__domains[domain] = []
        path_list = self.__domains[domain]
        exist = False
        for item in path_list:
            if item.path == path:
                item.cookies[pair[0]] = pair[1]
                exist = True
                break
        if not exist:
            path_cookies = PathCookies(domain,path)
            path_cookies.cookies[pair[0]] = pair[1]
            path_list.append(path_cookies)
    
    def del_cookie_item(self,domain,path,cookie_name):
        domain = domain.lower()
        path = path.lower()
        if self.__domains.has_key(domain):
            path_list = self.__domains[domain]
            for path_cookies in path_list:
                if path_cookies.path == path:
                    if path_cookies.cookies.has_key(cookie_name):
                        del path_cookies.cookies[cookie_name]
                        if len(path_cookies.cookies) == 0:
                            del path_cookies
                            if len(path_list) == 0:
                                del path_list
                        return
    def clear_domain(self,domain):
        domain = domain.lower()
        if self.__domains.has_key(domain):
            del self.__domains[domain]

    def clear(self):
        self.__domains.clear()

    def add_cookie_from_http_header(self,line,default_domain):
        segs = line.split(";")
        domain = default_domain
        path = None
        cookies = {}
        for item in segs:
            pos = item.find("=")
            if pos > 0 and pos < (len(item)-1):
                left = item[:pos]
                left = left.strip()
                right = item[pos+1:]
                right = right.strip()
                if left.lower() == "domain":
                    domain = right
                elif left.lower() == "path":
                    path = right
                elif left.lower() == "expires":
                    pass
                else:
                    cookies[left] = right
        if path and domain :
            path = path.lower()
            domain = domain.lower()
            if self.__domains.has_key(domain):
                path_list = self.__domains[domain]
                exist = False
                for path_cookies in path_list:
                    if path_cookies.path == path:
                        combine_map(path_cookies.cookies,cookies)
                        exist = True
                if not exist:
                    path_cookies = PathCookies(domain,path)
                    path_cookies.cookies = cookies
                    path_list.append(path_cookies)
            else:
                path_list = []
                path_cookies = PathCookies(domain,path)
                path_cookies.cookies = cookies
                path_list.append(path_cookies)
                self.__domains[domain] = path_list

    def gen_header_cookies(self,request_url):
        parse_result = urlparse.urlparse(request_url)
        domain = parse_result.netloc.lower()
        request_path = parse_result.path.lower()
        domain_list = []
        domain_list.append(domain)
        pos = 0
        while True:
            pos = domain.find(".",pos)
            if pos == -1:
                break
            domain_list.append(domain[pos:])
            domain_list.append(domain[pos+1:])
            pos += 1
        cookie_str = ""
        for item in domain_list:
            if self.__domains.has_key(item):
                path_list = self.__domains[item]
                for path_cookies in path_list:
                    if is_sub_path_i(path_cookies.path,request_path):
                        cookie_set = translate_map_to_cookie(path_cookies.cookies)
                        if cookie_set != "":
                            if cookie_str != "":
                                cookie_str += "; "
                            cookie_str += cookie_set
        return cookie_str

    def print_cookie(self):
        for domain in self.__domains.keys():
            path_list = self.__domains[domain]
            print "%s:" % domain
            for path_cookie in path_list:
                print "\t%s:" % path_cookie.path
                for cookie_key in path_cookie.cookies.keys():
                    print "\t\t%s=%s" % (cookie_key,path_cookie.cookies[cookie_key])


def combine_map(map1,map2):
    for key in map2.keys():
        value = map2[key]
        map1[key] = value

def translate_map_to_cookie(cookie_dict):
    result = ""
    for key in cookie_dict.keys():
        value = cookie_dict[key]
        if result == "":
            result = " %s=%s" % (key,value)
        else:
            result += "; %s=%s" % (key,value)
    return result


#ignore character case
def is_sub_path_i(path_parent,path_test):
    count = len(path_parent)
    if len(path_test) < count:
        return False
    return path_test[:count] == path_parent

if __name__ == "__main__": 
    pass

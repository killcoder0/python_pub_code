#!/usr/bin/python
# -*- coding:utf-8 -*- 
#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
import os
import platform

def get_cur_info_within_exception():
    f = sys.exc_info()[2].tb_frame.f_back
    filename = f.f_code.co_filename
    index = filename.rfind('/')
    if index < 0 :
        index = filename.rfind('\\')
    filename = filename[(index+1):]
    lineno = f.f_lineno
    return (filename,lineno)

def get_cur_info():
    try:
        raise Exception
    except:
        return get_cur_info_within_exception()

##the unit is G   (Only works on Linux)
#def get_disk_free(path):
#    import os
#    import platform
#    try:
#        stat = os.statvfs(path)
#        freesize = stat.f_bsize*stat.f_bfree/(1024*1024*1024)
#        return freesize
#    except OSError,e:
#        return -1

#get all local ip addresses (Only works on Linux)
def get_local_addr():
    import platform
    if platform.system() == "Linux":
        import subprocess
        ip_list = []
        content = subprocess.check_output(["/sbin/ifconfig|grep 'inet addr'|awk '{print $2}'"],shell=True)
        if not content or len(content) == 0:
            return ip_list
        index = 0
        start = -1
        while index < len(content):
            if content[index] == ':':
                start = index + 1
            elif content[index] == '\n' and start != -1:
                ip_list.append(content[start:index])
                start = -1
            index += 1
        return ip_list
    elif platform.system() == "windows":
        return []
    else:
        return []

#verify the ip
def is_ipv4_addr(ip):
    segs = ip.split(".")
    if len(segs) != 4:
        return False
    for seg in segs:
        try:
            value = int(seg)
            if value < 0 or value > 255:
                return False
        except ValueError,e:
            return False
    return True

#verify the port
def is_valid_port(port):
    try:
        value = int(port)
        if value < 0 or value > 65535:
            return False
    except ValueError,e:
        return False
    return True

#code below is just for testing
def test():
    info = get_cur_info()
    print info[0]
    print info[1]

#detect and create directory. WARNNING:this is not an atomic operation!!!!!!!!!!!!!!!
def test_directory(test_dir):
    if not os.path.exists(test_dir):
        try:
            os.mkdir(test_dir)
        except:
            return False
    elif not os.path.isdir(test_dir):
        return False
    if platform.system() != "Windows" and not os.access(test_dir,os.R_OK|os.W_OK|os.X_OK):
        return False
    return True



if __name__ == '__main__':
    test()
    print get_local_addr()
    os.system("pause")
import os

def is_filepath(line_txt):
    seg = "************* Module"
    return seg == line_txt[:len(seg)]

def is_warn_line(line):
    if is_filepath(line):
        return False
    return line[:3] == "W: " or line[:2] == "W:"

def is_record_line(line):
    if not line or len(line) < 3:
        return False
    return line[1] == ':'



if __name__ == '__main__':
    file_handler_t = open("check.log","r")
    filename_t = None
    line_t = None
    while True:
        line_t = file_handler_t.readline()
        if not line_t:
            break

        if is_filepath(line_t):
            filename_t = line_t
            continue
        if is_warn_line(line_t):
            if filename_t:
                print filename_t
                filename_t = None
            print line_t
            while True:
                line_t = file_handler_t.readline()
                if not is_record_line(line_t) or is_warn_line(line_t):
                    print line_t
                    continue
                elif is_filepath(line_t):
                    filename_t = line_t
                break
    file_handler_t.close()
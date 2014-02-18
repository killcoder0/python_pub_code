def is_filepath(line_txt):
#    return "E:\\" == line_txt[:3]
	return line_txt.find("************* Module") != -1

def is_err_line(line_txt):
    if is_filepath(line_txt):
        return False
    return line_txt[:3] == "E: " or line_txt[:2] == "E:"

def is_record_line(line_txt):
    if not line_txt or len(line_txt) < 3:
        return False
    return line_txt[1] == ':'



if __name__ == '__main__':
    file_handler = open("check.log","r")
    filename = None
    line = None
    while True:
        line = file_handler.readline()
        if not line:
            break

        if is_filepath(line):
            filename = line
            continue
        if is_err_line(line):
            if filename:
                print filename
                filename = None
            print line
            while True:
                line = file_handler.readline()
                if not is_record_line(line) or is_err_line(line):
                    print line
                    continue
                elif is_filepath(line):
                    filename = line
                break
    file_handler.close()
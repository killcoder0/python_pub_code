import os

for file in os.listdir("."):
    filename,ext = os.path.splitext(file)
    if ext == ".py":
        cmdline = "pylint %s" % file
        os.system(cmdline)

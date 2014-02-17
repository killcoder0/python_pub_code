import time

_start_id = int(time.time())

def get_new_id():
    global _start_id
    _start_id += 1
    return _start_id

_id_map = {}

def get_id(id_key):
    if not _id_map.has_key(id_key):
        return None
    return _id_map[id_key]

def set_id(id_key,id_value):
    global _id_map
    _id_map[id_key] = id_value
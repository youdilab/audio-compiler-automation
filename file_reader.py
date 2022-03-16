import os

def get_file_list(path):
    for (root,dirs,files) in os.walk(path, topdown=True):
        return files
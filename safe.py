"""
    version 0.1
    
    A useful library for making some of pythons design decisions more sensible by default
    eg: simply not making folders if they already exist
"""

from os import makedirs, path

from sys import version_info
import inspect

def resolve_get_args():
    if(version_info[0] == 2):
        return inspect.getargspec
    else:
        return inspect.getfullargspec


def make_dirs(new_path):
    if(path.exists(new_path)== False):
       makedirs(new_path)
       
        
# add lines for resolving urrlib, etc
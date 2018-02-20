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

from threading import Thread

def Thread(target, args = None, kwargs = None, daemon = True):
    
    if(version_info[0] == 2):
        
        if(args != None and kwargs != None):
            thread = Thread(target = target, kwargs = kwargs, args = args)
            thread.daemon = daemon
            return thread
        elif(args != None and kwargs == None):
            thread = Thread(target = target, args = args)
            thread.daemon = daemon
            return thread
        elif(args == None and kwargs != None):
            thread = Thread(target = target, kwargs = kwargs)
            thread.daemon = daemon
            return thread
        else:
            thread = Thread(target = target)
            thread.daemon = daemon
            return thread
    else:
        if(args != None and kwargs != None):
            return Thread(target = target, kwargs = kwargs, args = args, daemon = daemon) 
        elif(args != None and kwargs == None):
            return Thread(target = target, args = args)
        
        elif(args == None and kwargs != None):
            return Thread(target = target, kwargs = kwargs, daemon = daemon)
        else:
            return Thread(target = target, daemon = daemon)
        
# add lines for resolving urrlib, etc
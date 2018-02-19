#%%
from cache import *

#%%
import cache
reload(cache)
from cache import *

#%%
from time import sleep
def do_thing(a_arg):
    sleep(10)
    return a_arg

#%%
Memoize(do_thing)("hi")
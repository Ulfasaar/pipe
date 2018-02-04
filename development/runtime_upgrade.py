
# coding: utf-8

# In[47]:


# stores the results of all the steps up to maxsize anything over maxsize overwrites oldest data

# setting to 0 disables it

class Result_Cache:
    
    __slots__ = ("max_size", "size", "results", "to_replace")
    
    def __init__(self, max_size):
        self.max_size = max_size
        self.size = 0
        self.results = []
        self.to_replace = 0

    def append(self, result):
        
        if(self.max_size != 0):
            if(self.size < self.max_size):
                
                self.results.append(result)
                self.size = self.size + 1
               
            else:
                self.results[self.to_replace] = result
                self.to_replace = ( self.max_size - ( self.to_replace + 1 )) % self.max_size
            


# In[81]:


def check_external(step):
    return step.__name__ == "is_external" and step.__module__ == "pipe"


# In[84]:


cache = Result_Cache(2)
cache.append(1)
cache.append(2)
cache.append(3)
cache.append(4)
cache.append(5)
# cache.append(6)
# cache.append(7)
# cache.append(8)
# cache.append(9)
# cache.append(10)
cache.results


# In[ ]:


# if the step is external rerun it and compare its value to the value in the cache

# how do I know if its value is in the cache if we jump forward?

# maxsize cannot be smaller than the length of the pipe otherwise there is no benefit because there would be no data
# to compare against 

# how would we compare non hashable values such as dask pointers?

# this would also cause a memory explosion if all the steps manipulate the same multi gigabyte data due to its
# compounding nature

# solution: only store the last result, and any result that comes just before a external step


# In[85]:


step_queue = []

# serves as a marker for caching system
# during run check to see for any steps with the __name__ is_external from module pipe mark index
def check(step):
    def is_external(data):
        return step(data)
    return is_external


# In[7]:


import cache


# In[44]:


from safe import resolve_get_args

class Pipe:
    
#     slots to make things more efficent
    __slots__=("steps", "name", "start_value")
    
    def __init__(self, *steps, **kwargs):
        self.name = kwargs.get("name", None)
        
        steps = list(steps)
        
#         steps = fix_pipe_arg(*steps)

        if callable(steps[0]):
            self.steps = steps
            self.start_value = None
        else:
            self.start_value = steps[0]
            self.steps = steps[1:]
            
    def append(self, *steps):
        self.steps += steps
        
    def insert(self, index, step):
        self.steps = self.steps.insert(index, step)
        
    def replace(self, index, step):
        self.steps[index] = step

    def open(self, data=None):
        
        def get_result(step, data):
            args = get_args(step).args
            num_args = len(args)
            
            if num_args == 1 or (num_args == 2 and args[0] == "self"):
                return step(data)
                
            elif num_args > 1:
                return step(*data)
            
            if(callable(step)):
                return step()
            else:
                return step
        
        prev_result = None
        get_args = resolve_get_args()

        if self.start_value != None:
            if(data == None):
                data = self.start_value
            else:
                print("WARNING! you put a raw value at the top of your pipe and you put " + str(data) + " in the opening of the pipe the value at the start of the pipe has been overwritten by the passed in value. You may want to get rid of that value at the top of the pipe to get rid of this message\n")
            
        if(len(self.steps)> 0):
            if data != None:

                prev_result = get_result(self.steps[0], data)

            else:
                prev_result = self.steps[0]()
        else:
            return data
     
        for step in self.steps[1:]:
            prev_result = get_result(step, prev_result)

        # the use is multithreading so add the result to the pool of data
        if(self.name != None):
            global pool
            pool.update({self.name: prev_result})

        return prev_result
        


# In[36]:


from pipe import *


# In[35]:


import pipe
reload(pipe)


# In[39]:


def blah():
    return "hi"

testee = Pipe(blah)

test = Pipe(testee.open, name="blah")


# In[40]:


join(parallel(test))


# In[18]:


import safe as sf


# In[25]:


reload(sf)


# In[4]:


test.open("hi")


# # testing pipe caching

# In[6]:


import cache


# In[7]:


from time import sleep

def long_method():
    sleep(10)
    return "hello"

# test2 works beautifully, no idea why must be binding the cache to the pipe or something
test2 = Pipe(
            cache.Cache(long_method).get
        )

# test 3 returns a cache cus why not

test3 = Pipe(
            lambda : cache.Cache(long_method)
        )

test4 = Pipe(
            long_method
        )


# In[9]:


test2.open()


# In[10]:


temp = test3.open()
temp.get()


# In[11]:


temp.get()


# In[12]:


test_cache = cache.Cache(test4.open)


# In[14]:


test_cache.get()


# In[15]:


# testing speed

Pipe(
    "hola"
).open("seniorita")


# # creating an upgraded stream function

# goals: 
# 1. make the tasks transparent for things like test
# 2. make it fast
# 3. make it more memory effecient by assuming the supplied list is immutable and use a generator

# In[111]:


from pipe import *


# In[110]:


import pipe
reload(pipe)


# In[112]:


mutable_stream = stream


# In[178]:


# define a run function, stream function will return the run function for the stream object

class __Stream(object):
    __slots__ = ("pipe")
    
    def __init__(self, *steps):
        self.pipe = Pipe(*steps)
    
    def run(self, data):

        for item in data:
            yield self.pipe.open(item)
            
#         while(len(data) > 0):

#             result = self.pipe.open(data[0])
#             del data[0]

#             yield result

            
# old stream becomes mutable_stream
def stream(*steps):
    return __Stream(*steps).run


# In[97]:


# this is how we get the steps out of the stream for testing now might cause issues in python 3


# In[101]:


stream(hi).__self__.pipe.steps


# In[142]:


def hi(message):
    return message + "hi"
    
temp = ["be", "ro", "me"]
streamed = stream(hi)(temp)


# In[115]:


temp2 = ["be", "ro", "me"]


# In[143]:


get_ipython().magic(u'timeit mutable_stream(hi)(temp2)')


# In[168]:


test = Pipe(
        mutable_stream(hi)
    )


# In[169]:


get_ipython().magic(u'timeit test.open(["be", "ro", "me"],)')


# In[146]:


for item in streamed:
#     continue
    print item, temp


# In[90]:


# useful? decide later if it should be in pipe lib probs not, they can use a mutable stream if they don't like generators
def aggregate(gen):
    return list(gen)


# In[147]:


def speak(data):
    return list(data)


# In[179]:


# the equivalent thing to older mutable stream, takes longer to process by 10 microseconds also cannot support
# having a constant at the top of the pipe as it gets destroyed after the first run, or you have to assume it runs
# only once after declaration, should be more memory effecient however and provide a faster way to process things than 
# dask since its all in memory however the initial dataset has to fit in memory and will then be drained whilst
# its running

test = Pipe(
    stream(
        hi
    ),
    speak
    
)


# In[ ]:


# debating if this upgrade is worth it since it makes things run slower


# In[ ]:


# hmmmm runs slightly faster without delete command, put this idea on hold for now and come back later once
# all goals can be met


# In[181]:


get_ipython().magic(u'timeit test.open(["be", "ro", "me"])')


# # Javascript

# Consider transpiling existing code using my own translator or a open source one
# 
# Consider writing as seperate library to handle event streams, make a leaner runtime etc thanks to javascript niceties

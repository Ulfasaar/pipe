
# coding: utf-8

# In[1]:


from pipe import *


# In[12]:


def test(arg1, arg2):
    print(arg1)


# In[13]:


Pipe(test).open(["hi", "there"])


# Make my own function to draw using matplotlib because networkx is horrible

# Fix the balancer

# In[3]:


# Trick to prevent annoying autosave spamming with messages due to time lags in docker
get_ipython().magic(u'autosave 0')


# In[4]:


def say_hello(data):
    print(data)

run_concurrently(say_hello)(["hi", "hello", "hola"])


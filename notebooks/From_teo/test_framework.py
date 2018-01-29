
# coding: utf-8

# A brand new testing framework. Ideally it will be passed a pipe, some input and a list of expected outputs so that it can test all the steps and the whole pipe????

# should also allow us to run tests using just a function, maybe even just make a pipe of tests and it runs and sees if it all equals if it doesn't equal it errors and returns the one that failed and throws exception

# Currently the testing framework will test individual pipes and run a series of tests on that pipe,
# 
# tests are defined as lists with the first input being the input for the pipe and all the subsequent members being the expected outputs at each stage of the pipe, these tests are themselves contained in a list of tests to run

# In[71]:


from IPython.display import Markdown, display

def pretty_print(message, style):
    if(style == "bold"):
        display(Markdown("<bold>" + message + "</bold>"))
    elif(style == "red"):
        display(Markdown("<font color='red'>" + message + "</font>"))
    elif(style == "green"):
        display(Markdown("<font color='green'>" + message + "</font>"))

def test(pipe, tests):
#         init()
        correct_count = 0
        wrong_indeces = {}
        
#         iterate over all three lists at the same time

#   if the stage gives the expected output then add one to correct count display nice count of num failed passed at top
#   display list of failed steps would be nice if it gave detailed info but will work on that
        
        for test in tests:
    
            for i, task in enumerate(pipe.steps):
                datum = test[0] 
                expected = test[i+1]
                actual = task(datum)
                
                if( actual == expected):
                    correct_count+= 1

                else:
                    wrong_indeces[i] = {"input": datum, "expected": expected, "actual": actual}
        
     
        for index in wrong_indeces:
            message = "Failed at stage: {}, actual {}, expected {}, for input {}".format(index, wrong_indeces[i]["actual"],
                                                                                        wrong_indeces[i]["expected"], datum)
            pretty_print(message, "red")
            
        failed_count = (len(pipe.steps) * len(tests)) - correct_count
        
        pretty_print("Tests passed {}, failed {}".format(correct_count, failed_count), "green")
       


# For now streamers can't be introspected and have to be black boxed, individual steps can be pulled out of the class and tested on their own however, not a train smash just need to pull them out and shove them in their own pipe and only feed one thing for now

# In[40]:


from pipe import *

def display_message(message):
    return message

def display_extra(message):
    return message + "hehehehhe" 

test1 = Pipe(display_message, display_extra)


# In[ ]:


# write each test as a list in the order it is expected to occur eg [input, stage 1, stage 2 etc]
# make a list of these lists
# make a load balancer


# In[73]:


test(test1, [["hi", 'hi', 'hihehehehhe'], ['bye','bye', 'byehehehehhe']])


# issue streamers etc cannot be ingested ATM because they are functions so have no variables stored in them

# In[1]:


import nose


# In[7]:


# Trick to prevent annoying autosave spamming with messages due to time lags in docker
get_ipython().magic(u'autosave 0')


# In[3]:


import pytest


# In[2]:


from pipe import *


# In[5]:


from pipe import *

def display_message(message):
    print(message)
    return message

def display_extra(message):
    print(message + "hehehehhe")
    return message + "hehehehhe" 
    
test1 = Pipe(
            ["hi", "bye"],
            stream(
                display_message,
                display_extra,
            )
        )
test2 = Pipe(
     ["hi", "bye"],
            stream(
                display_message,
                display_extra,
            )
)

test3 = Pipe(
        stream(
            display_message,
            display_extra,
        )
    )




test1.open(["hi", "bye", "farewell"])

test2.open()

test3.open(["hi", "bye"])


# In[2]:


test4 = Pipe(
            display_message
        )

test4.append(display_extra)

test4.open("hi")

test5 = Pipe(
            display_message
        )

test5.replace(0, display_extra)

test5.open("hi")


# In[75]:


def hello_1():
    return 1

def say_hello(num):
    print("hello" + str(num))
    return num

def say_goodbye(num):
    print("goodbye" + str(num))
    return num
    
test_pipe1 = Pipe(
                hello_1,
                say_hello,
                say_goodbye,
                name = 'hi1'
            )

def hello_2():
    return 2

test_pipe2 = Pipe(
                hello_2,
                say_hello,
                say_goodbye,
                name = 'hi2'
            )

running = parallel(test_pipe1, test_pipe2)
join(running)


# In[4]:


pytest


# In[5]:


get_ipython().magic(u'pinfo pytest')


# Consider making each test a function that returns a equality operator, this gets passed to a test pipe, test pipe just tests each function one by one adds up passes which would be true and falses which are fails and records failed indexes
# 
# diplays lists of errors hopefully with test names, expected and actual???
# 
# says how many failed and how many passed
# 
# functions just return tuples like ( actual, expected, actual == expected )  get funcnt name by retrieving .__name__

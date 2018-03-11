#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x1b9c7ba2

# Compiled with Coconut version 1.2.2 [Colonel]

"""
Pipes provide a nice way to lazily queue steps for later execution and allow for a nice way to chain together sequential functions. They also provide many other benefits listed below along with their usage information

Pipes can accept raw values at their tops but nowhere else in the pipe as that would break the flow and be pointless 

EG: Pipe(
        "hi",
        display_message,
        display_farewell
    )
    
not 

Pipe(
        "hi",
        display_message,
        "bye",
        display_farewell
    )

Pipes also accept arguments in their open function removing the need for a complex step in the pipe that pulls the data in if that is not desired.

EG:

test = Pipe(

       display_message,
       display_farewell
       )
       
test.open("hi")

This also allows pipes to be joined together in succession like so, and intermingle them with the rest of the pipe

test2 = Pipe(
            really_goodbye
        )

test3 = Pipe(
        test.open,
        test2.open
        )


It also makes it easy to perform unit and integration tests as each part of the pipe should be quite small in size. To perform a integration test one just needs to get the pipe and to open it and see if the outputted result is what they expect.

Use the name prop if you want to run the pipes in parallel so that the resulting data can be identified and aggregated by the join part. If you are not concerned with the outputs of the pipe and just want to run them in parallel then the name isn't necessary

Sources or input parts are parts of a pipe that take no arguments and produce some data. These are usually used to interact with a external data source like a file, an API, the user or a database

Outlets or output parts are parts of a pipe that have no proceeding parts following them which results in the processed data being released to whatever other storage is waiting on the other end when the pipe is opened  

Pipe segments are pipes that are used to construct a larger pipe. Kind of like a subtree within a tree

Pipes can be serialised as well allowing for easy reuse.

You may want to consider a different structure if your problem is mostly asynchronous in nature or if you have to process variable amounts of data as large amounts of data on weak hardware can cause pipe blockages. You may want to consider the master slave architecture proposed by Google or, you may want to create a individual pipe for each unit within the batch and run said pipes in parallel to avoid blockages.

"""

# Coconut Header: --------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_compose, _coconut_pipe, _coconut_starpipe, _coconut_backpipe, _coconut_backstarpipe, _coconut_bool_and, _coconut_bool_or, _coconut_minus, _coconut_tee, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: ------------------------------------------------------



from version_safe import resolve_get_args

class Pipe(object):

#     slots to make things more efficent
    __slots__ = ("steps", "name", "start_value")

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
        self.steps.insert(index, step)

    def replace(self, index, step):
        self.steps[index] = step

    def open(self, data=None):

        @_coconut_tco
        def get_result(step, data):
            args = get_args(step).args
            num_args = len(args)

            if num_args == 1 or (num_args == 2 and args[0] == "self"):
                raise _coconut_tail_call(step, data)

            elif num_args > 1:
                raise _coconut_tail_call(step, *data)

            if (callable(step)):
                raise _coconut_tail_call(step)
            else:
                return step

        prev_result = None
        get_args = resolve_get_args()

        if self.start_value != None:
            if (data == None):
                data = self.start_value
            else:
                print("WARNING! you put a raw value at the top of your pipe and you put " + str(data) + " in the opening of the pipe the value at the start of the pipe has been overwritten by the passed in value. You may want to get rid of that value at the top of the pipe to get rid of this message\n")

        if (len(self.steps) > 0):
            if data != None:

                prev_result = get_result(self.steps[0], data)

            else:
                prev_result = self.steps[0]()
        else:
            return data

        for step in self.steps[1:]:
            prev_result = get_result(step, prev_result)

# the use is multithreading so add the result to the pool of data
        if (self.name != None):
            global pool
            pool.update({self.name: prev_result})

        return prev_result

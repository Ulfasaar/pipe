"""
version 0.1


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

eg:

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

from safe import resolve_get_args

class Pipe(object):
    
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
        
        
# returns a deep copy of the pipe that is passed to it         
def copy(pipe):
    return Pipe(*pipe.steps)        

# Limiter, it only allows x number of things from the previous stage to the next one

def limit(limit):
    def limiter(data):
        
        if limit > 1:
            return data[:limit]
        elif limit == 1:
            return data[0]
        elif limit == 0:
            return None
                
    return limiter

# Repeater, repeatedly calls a function with the same arguments x times
def repeat(function, times):
#     fix_pipe_arg(function)
    
    def repeater(args):
        results = []
        for i in range(times):
            results.append(function(args))
        return results
    
def fix_pipe_arg(*args):
    """Use this function so that if a pipe is passed to it it will automatically use its open function wprk in progress"""
    
    print(args)
    new_args = []
    for arg in args:
        
        if(type(arg) is Pipe):
            new_args.append(arg.open)
        else:
            new_args.append(arg)
    return new_args


# Validator, runs check_validity function which must return true or false depending on whether or not the data is valid, if it is valid then it will return the input data, if it is not valid it will execute another function to get the corrected result

def validate(check_validity, on_success = None, on_fail = None):

#     fix_pipe_arg(check_validity, on_success, on_fail)

    def validator(data):
        
        if(check_validity(data)):

            if(on_success != None):
                return on_success(data)
            else:
                return data
        else:
            if(on_fail != None):
                return on_fail(data)
            return None
    return validator


# Parallel runs all the pipes listed at the same time, concurrently

# parallel accepts a optional list of arguments to be passed to each pipe

from safe import Thread

def parallel(*pipes, **kwargs):
    args = kwargs.get("args", None)
    threads = []
    for i, pipe in enumerate(pipes):
        
        if(args != None):
            thread = Thread(target=pipe.open, kwargs = {'data':args[i]})
        else:
            thread = Thread(target=pipe.open)
            
        thread.start()
        threads.append(thread)
    return threads

def run_parallel(*pipes):
    """A wrapper to make the parallel function play nice with pipes it currently does not support passing args to pipes open
        function
    """
    
    def parallel_runner():
        
        return parallel(*pipes)
    return parallel_runner

# Join pipes waits for all the pipes to stop flowing and then closes them off.
# pool is a dictionary so we can pull out the results of the joining regardless of order :)
pool = {}

# this could be improved to accept pipes, store the threads as a dictionary where the memory address is the key and 
# the value is the thread, means we can do like join(pipe1, pipe2) etc

# for now it just assumes that it will receive the raw threads from the previous step

def join(threads):
    global pool
    
    # join all the threads so we wait for all the threads to finish
    for thread in threads:
        thread.join()
        
    # free memory
    del threads[:]
       
    temp_pool = pool.copy()
    pool.clear()
    return temp_pool

# The streamer will iterate over each item that is passed to it inside a pipe and pass it to each step one by one
# this makes the code for steps a lot cleaner and improves performance by removing the need to iterate over a batch
# several times
# please note that if you want to create a online based continous pipeline then you should just create a normal pipe where all the stages expect the data to be individual values, then you continuolly feed it new data and retrieve the resulting output

# this is due to the fact that the streamer assumes that there is a finite number of items in the data it is iterating over and then accumulates the result and returns it. It does not expect a infinite data source such as a generator.

def stream(*steps):
    def streamer(data):
        
        # transparently create a pipe
        pipe = Pipe(*steps)
        
        # iterate through and put items into the pipe one by one
        results = []
        for item in data:
            print(item)
            results.append(pipe.open(item))
        
        return results
            
    return streamer

# converts a dictionary with a numeric index into a list of results sorted by the key
def dict_to_list(mydict):
    results = []
    for key in sorted(mydict.keys()):
        results.append(mydict[key])
    
    return results

# this function will run multiple instances of a pipe in parallel and gives each pipe a split of the data it receives so that each chunk contains the number of items specified

# this is useful for scenarios where a large load needs to be processed in parallel to alleviate blockages in a pipe
# and for processing individual items in a dataset in parallel for super performance boosts
def balance(pipe, chunks_size):
    def balancer(data):
        
        if(chunks_size > 1):
            increments = list(range(chunks_size, len(data), chunks_size))

            pipes = [copy(pipe) for i in range(len(increments)) ]

            # label pipes

            for i, ipipe in enumerate(pipes):
                ipipe.name = i

            args = [data[:increments[0]]]
            for i, increment in enumerate(increments[1:]):
                args.append(data[increments[i]:increment])

            return parallel(*pipes, args=args)
        
        elif chunks_size == 1:
            def label_copy(pipe, index):
                new_pipe = copy(pipe)
                new_pipe.name = index
                return new_pipe

            pipes = [label_copy(pipe,i) for i in range(len(data)) ]
            
            # label pipes
            for i, ipipe in enumerate(pipes):
                ipipe.name = i

            return parallel(*pipes, args=data)
        else:
            raise Exception("Chunk size must be 1 or larger for balancer")
            
    return balancer


# Simple balance is a shorthand for the balance function that automatically waits for the threads to finish and then aggregates
# the results and converts them into a list of result chunks, only needed if you want to get the results easily
def simple_balance(pipe, chunk_num):
    
    balance_load = Pipe(
                balance(
                    pipe,
                    chunk_num
                ),
                join,
                dict_to_list
            )
    
    return balance_load.open

# not to be confused with parallel
# this function will split a list into individual items and run the steps as a pipe on each item concurrently
# it will then automatically aggregate the results into a list that is ordered the same as the items in the input

# this is a even simpler to use function than the simple_balance function

# great for scenarios where you want to just run many copies of one pipe and have everything managed
def run_concurrently(*steps):
    return simple_balance( Pipe( *steps ), 1)

from os import path

def checkpoint(fname, fformat = "csv", mode="a+"):
    """
        This super special function fires off a worker thread to write a dataframe to a specified CSV file in a non blocking
        way. In the future it will support alternative file formats and other data types besides pandas dataframes.
    """
    def __checkpoint(data):
        
        if(path.isfile(fname)):
            with open(fname, mode) as my_file:
                data.to_csv(my_file, header=False)
        else:
            data.to_csv(fname)
    
    # assume data is a dataframe for now, add if clauses for other if statements later
    def checkpointer(data):
        
        # later this will checkpoint all the tasks passeed to this too
        
        # create fire and forget thread
        Thread(target=__checkpoint, kwargs = {'data':data}).start()
        
        # return data so we can keep going
        return data
    
    return checkpointer

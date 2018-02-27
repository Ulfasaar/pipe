        
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
           results.append(pipe.open(item))
        
        return results
            
    return streamer

# converts a dictionary with a numeric index into a list of results sorted by the key
def dict_to_list(mydict):
    results = []
    for key in sorted(mydict.keys()):
        results.append(mydict[key])
    
    return results

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
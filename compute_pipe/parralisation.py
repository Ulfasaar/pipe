# Parallel runs all the pipes listed at the same time, concurrently

# parallel accepts a optional list of arguments to be passed to each pipe

from version_safe import Thread

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
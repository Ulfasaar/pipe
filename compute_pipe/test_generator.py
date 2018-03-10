
# some arbritary functions
def add_1(num):
    return num + 1

def add_2(num):
    return num + 2

# same as a pipes steps
funct_list = [add_1, add_1, add_1, add_2]

# this will be used to turn our steps into a queue
gen = (x for x in funct_list)

# executing some steps and then interrupting the execution
for i, funct in enumerate(gen):
    print(funct(1))
    if i == 2:
        break

# changing the definition of a function

changed_function = u"""def add_2(num): 
    return num + 3"""

# pretty printing for debugging
print(changed_function + "\n")

# showcasing how it will change at runtime
exec(changed_function)

#sigh python at compile time is fine but runtime is having a fit

# will probably have to store runtime code in a seperate file then use reload(pipe_def)
# to change it whilst it is live

# updating the steps definition
funct_list[-1] = add_2

# resuming execution with the same queue
for i, funct in enumerate(gen):
    print(funct(1))



# a better solution
## define a step class, this class will hold whether or not it has been run already to track progress
# biggest headache would be finding a way to easily keep the has_run prop up to date
# however has less overhead than generators and would mean that we would have proper progress tracking

## actually the for in loop won't run if the generator is empty so I guess it works?????



# OMG it works!!!! We can update a system whilst its live B)

# stub execution with pausing capacity

# this has to somehow sit outside the thing that actually executes the steps otherwise we risk overwriting it on resume
# which means we lose the progress thus far
# step_gen = (x for x in self.steps)

# outer if is to prevent items being wasted in the generator

# open will have to be executed inside a thread such as parallel
# if(pause == False):
#     for step in step_gen:
#         # run return result etc
#         # if paused after a step break
#         if(pause):
#             break



# coding: utf-8

# In[138]:


from pipe import *


# In[218]:


sample = None

with open("compiler.[]", 'r') as raw:
    sample = raw.read()


# In[180]:


# print(sample)

# add support for classes with nice syntax for abstract 
# data types

# could rewrite the compiler in nim so that it is a smaller executable more effecient etc

# In[226]:


import re


# In[230]:


def split_lines(raw_text):
    
    lines = raw_text.split('\n')
#     print("raw lines\n")
#     print(lines)
    # optimise to remove all at once using stream or somthing else
    while '' in lines: lines.remove('')
        
    # removes whitespace lines of any length
    
    result = []
    for line in lines:
        if(re.match(r"^ +$", line)):
            continue
        else:
            result.append(line)
    
    lines = result
#     while  in lines: lines.remove(r"^ +$")
        
        
#     while ' ' in lines: lines.remove(' ') 
    while '\t' in lines: lines.remove('\t')
#     print('\nwithout blank tokens\n')
#     print(lines)
    return lines

def group_defs(lines):
    # somehow group the lines together to resemble definitions
    # look for return statement?
    chunks = []
    
    chunk = []
    
#     print("\ngrouping\n")
#     print(lines)
    
    for line in lines:
        chunk.append(line)
    
#         return marks the end of chunk for now, later it will just be end of tabbing
# how to handle special pipe lines>
        if ('return' in line) and '#' not in line and "'return'" not in line:
            chunks.append(chunk)
            chunk = []
            
    # scan from the bottom up to construct pipe
    lines.reverse()
    
    pipe_chunk = []
    
    for line in lines:
        if('return' in line):
            break
        else:
            pipe_chunk.append(line)
        
    return chunks, pipe_chunk
            
def compile_defs(chunks, pipe_chunk):
    
    for i, lines in enumerate(chunks):
    
        # change arguments so that they are comma seperated
        tokens = lines[0].split(' ')

        name = tokens[0]
        args = ','.join(tokens[1:])

        lines[0] = "def " + name + "(" + args + "):"
        
        chunks[i] = lines
    return chunks, pipe_chunk

def compile_pipe(chunks, pipe_chunk):
    result = []
    
    for line in pipe_chunk:
        result.append(line + ',')
        
    # need to find a way to insert this at this step instead of passing it through
    # assume if it is not given that it is the file name
    name = "compiler"
        
    result.insert(0, name + ' = __pipe__.Pipe(')
    result.append(')')
    chunks.append(result)
    return chunks
    

def join_lines(chunks):
    
    result = []
    
    for lines in chunks:
        lines.append('\n')
    
    for lines in chunks:
        result.append('\n'.join(lines))
    return '\n'.join(result)

def import_pipe(result):
    return "import pipe as __pipe__\n\n" + result


# Write awesome syntax highlighter here that outputs the colors for the python code to make it more legible

# In[146]:


from IPython.display import Markdown, display

def pretty_print(text):
    display(Markdown("```python\n" + text + "\n```"))


# In[231]:


compiler = Pipe(
    split_lines,
    group_defs,
    compile_defs,
    compile_pipe,
    join_lines,
    import_pipe
)

# code = join_lines(compile_defs(split_lines(sample)))

code = compiler.open(sample)


# In[232]:


display(Markdown('**Generated code:**'))
pretty_print(code)


# Have to bootstrap the above somehow to support other languages

# basic interpreter for now neat idea allows for testing code in notebook

# In[66]:


exec compile(code, "<string>", "exec")


# In[67]:


hi("blah", "bleh")


# Better to write it to file

# In[70]:


with open('sample.py', "w+") as dest:
    dest.write(code)


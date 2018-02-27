from compute_pipe import *
import pytest

def test_basic():
    def hi():
        return "hi"

    assert Pipe(hi).open() == "hi"

def test_complex():
    def say_hello(message):
        return "hello " + message

    assert Pipe('Bob', say_hello).open() == 'hello Bob'

def test_steps():
    def funct1():
        return 1

    def funct2():
        return 2

    test = Pipe(funct1, funct2)

    assert type(test.steps) == list

def test_insert():
    def funct():
        return 1
    
    def funct2():
        return 2
    
    def funct3():
        return 3

    a_pipe = Pipe(funct, funct3)

    a_pipe.insert(1, funct2)
    assert a_pipe.steps == [funct, funct2, funct3]

def test_replace():
    def funct():
        return 1
    
    def funct2():
        return 2
    
    def funct3():
        return 3

    a_pipe = Pipe(funct, funct2, funct3)

    a_pipe.replace(1, funct)

    assert a_pipe.steps[1] == funct

def test_copy():
    def funct():
        return 1
    
    def funct2():
        return 2
    
    def funct3():
        return 3

    a_pipe = Pipe(funct, funct2, funct3)
    second_pipe = copy(a_pipe)

    assert a_pipe is not second_pipe

def test_limit():
    test = Pipe([1, 2, 3 ,4], limit(2))
    actual = test.open()
    assert actual == [1, 2]

def test_append():
    def funct():
        return 1
    
    def funct2():
        return 2
    
    def funct3():
        return 3

    test = Pipe(funct, funct2)
    test.append(funct3)

    assert test.steps[-1] == funct3

def test_append_collection():
    def funct():
        return 1
    
    def funct2():
        return 2
    
    def funct3():
        return 3

    test = Pipe(funct)
    test.append(funct2, funct3)

    assert test.steps == [funct, funct2, funct3]

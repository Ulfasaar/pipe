import pipe as pp

def hello(name):
    return "hello " + name

test = pp.Pipe(hello)

from multiprocessing import freeze_support

if name == "__main__":
    freeze_support()
    pp.parallel(test, test)
# pp.simple_balance(test, 1)(["Steve", "Bob"])
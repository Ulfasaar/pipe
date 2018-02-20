import pipe as pp

def hello(name):
    return "hello " + name

test = pp.Pipe(hello)

pp.parallel(test)
# pp.simple_balance(test, 1)(["Steve", "Bob"])
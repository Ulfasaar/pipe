from compute_pipe import *
import unittest

class TestPipe(unittest.TestCase):

    def test_basic(self):
        def hi():
            return "hi"

        self.assertEquals( Pipe(hi).open(), "hi")

    def test_complex(self):
        def say_hello(message):
            return "hello " + message

        self.assertEquals(Pipe('Bob', say_hello).open(), 'hello Bob')

    def test_steps(self):
        def funct1():
            return 1

        def funct2():
            return 2

        test = Pipe(funct1, funct2)

        self.assertIsInstance(test.steps, list)

    def test_insert(self):
        def funct():
            return 1
        
        def funct2():
            return 2
        
        def funct3():
            return 3

        a_pipe = Pipe(funct, funct3)

        a_pipe.insert(1, funct2)
        self.assertListEqual(a_pipe.steps, [funct, funct2, funct3])
    
    def test_replace(self):
        def funct():
            return 1
        
        def funct2():
            return 2
        
        def funct3():
            return 3

        a_pipe = Pipe(funct, funct2, funct3)

        a_pipe.replace(1, funct)
        self.assertEqual(a_pipe.steps[1], funct)

    def test_copy(self):
        def funct():
            return 1
        
        def funct2():
            return 2
        
        def funct3():
            return 3

        a_pipe = Pipe(funct, funct2, funct3)
        second_pipe = copy(a_pipe)
        self.assertNotEqual(a_pipe, second_pipe)

    def test_limit(self):
        test = Pipe([1, 2, 3 ,4], limit(2))
        actual = test.open()
        self.assertListEqual(actual, [1, 2])


if __name__ == '__main__':
    unittest.main()
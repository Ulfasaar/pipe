from tkinter import *

root = Tk()
root.title('Pipe editor')

# read in a pipe [] file and display

T = Text(root, height=40, width=100)
T.pack()

with open('../compiler.[]', 'rb') as text:
    T.insert(END, text.read())


# T.insert(END, "Just a text Widget\nin two lines\n")
mainloop()
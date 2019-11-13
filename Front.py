from tkinter import *
import os
from time import sleep
from threading import Thread
from tkinter import filedialog


root = Tk()
root.title("EMT")
root.geometry('300x300')
root.resizable(width=False, height=False)

entryText_input = StringVar()
entry_input = Entry(root, textvariable=entryText_input)
entry_input.place(x=60, y=27)

entryText_output = StringVar()
entry_output = Entry(root, textvariable=entryText_output)
entry_output.place(x=60, y=57)

entry_file = Entry(root)
entry_file.place(x=60, y=87)

run = Button(root, text="Run!")
run.bind('<Button-1>', lambda event: Run())
run.place(x=120, y=150)

label_input = Label(root, text="Model:")
label_input.place(x=10, y=30)

label_output = Label(root, text="Output:")
label_output.place(x=6, y=60)

choose_input = Button(root, text=" ... ")
choose_input.place(x=260, y=30)
choose_input.bind('<Button-1>', lambda event: openfile())

choose_output = Button(root, text=" ... ")
choose_output.place(x=260, y=60)
choose_output.bind('<Button-1>', lambda event: outputfile())

label_filename = Label(root, text="File:")
label_filename.place(x=26, y=90)



def openfile():
    newtext = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("excel files", "*.xlsm"), ("all files", "*.*")))
    entryText_input.set(newtext)


def outputfile():
    newtext = filedialog.askdirectory()
    entryText_output.set(newtext)


def disable():
    run['state'] = 'disabled'
    run.update()


def enable():
    run['state'] = 'normal'
    run.update()


def Run():
    disable()
    full = os.path.abspath('main.py')
    full = full[0:len(full) - 7]
    os.system('cd ' + full)
    os.system('python3 main.py' + ' ' + entry_input.get() + ' ' + entry_output.get() + ' ' + entry_file.get() + '.xls')
    enable()


root.mainloop()

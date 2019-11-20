import subprocess
from threading import Thread
from time import sleep

def f():
    subprocess.run(['python3', 'main.py', 'fill', '/Users/egormatveev/PycharmProjects/VBA2Python/models/book2x1.xlsm', '/Users/egormatveev/Desktop', 'testresss.xls', '1000', 'True'])


class mythread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        f()


a = mythread()
b = mythread()
a.start()
print('run a')

b.start()
print('run b')
from z3 import *
from threading import Thread

def getValue(model, param):
    values = str(model).replace('[', '').replace(']', '').split(', ')
    for i in values:
        if i.__contains__(param):
            return i.split(' = ')[1]

s = Solver()
x = Int('x')
s.add(x == 1000)
if s.check() == sat:
    print(getValue(s.model(), 'x'))
else:
    print('no')
from z3 import *


a = Int('a')
b = Int('b')
solve(a ** b == b ** a)

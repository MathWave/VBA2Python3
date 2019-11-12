import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from z3 import *

s = Solver()
arr = []
for i in range(100):
    arr.append(Int('x' + str(i)))
s.add(x)
s.check()
print(s.model())


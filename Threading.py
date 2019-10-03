from threading import Thread
from z3 import *


class CalcNodeFirst(Thread):

    def __init__(self, count, X, intgraph):
        super().__init__()
        self.count = count
        self.X = X
        self.condition = []
        self.intgraph = intgraph

    def run(self):
        self.condition = [Or([And(self.X[self.count] == j, self.X[self.count + 1] == k)
                     for j in self.intgraph.keys() for k in self.intgraph[j]])]

    def start(self):
        self.run()


class CalcEilerFirst(Thread):

    def __init__(self, count, X, intgraph):
        super().__init__()
        self.count = count
        self.X = X
        self.condition = []
        self.intgraph = intgraph

    def run(self):
        self.condition = [Or([And(self.X[k] == self.count[0], self.X[k + 1] == self.count[1])
                              for k in range(len(self.X) - 1)])]

    def start(self):
        self.run()
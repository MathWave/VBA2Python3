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

'''
class FindEdges(Thread):

    def __init__(self, fullgraph, partgraph):
        super().__init__()
        self.fullgraph = fullgraph
        self.partgraph = partgraph
        self.add = {}
        for i in partgraph:
            self.add[i] = []

    def run(self):
        arr = GetParamsArray(info)
        count = 0
        for node in self.partgraph:
            for node2 in self.fullgraph.keys():
                if node2 not in self.fullgraph[node]:
                    s = Solver()
                    cond = []
                    cond.append(z3_funcs.GetHyperState(*arr[0:info[0]]) == StringVal(node))
                    cond.append(z3_funcs.GetHyperState(*arr[info[0]:info[0] * 2]) == StringVal(node2))
                    cond.append(z3_funcs.IsPossible(*arr[0:info[0]], *arr[info[0] * 2::]))
                    cond += [z3_funcs.NextCurrent(arr[0:info[0]], arr[info[0] * 2:info[0] * 2 + info[1]])[i] == arr[
                        info[0] + i] for i in range(info[0])]
                    s.add(cond)
                    checker = 0
                    try:
                        checker = s.check()
                    except:
                        print('sosatb')
                    if checker == sat:
                        self.add[node].append(node2)
                    count += 1
                    #print('ready ' + str(count / len(graph.keys()) ** 2 * 100) + ' %')


class FindNodes(Thread):

    def __init__(self, fullgraph, partgraph):
        super().__init__()
        self.fullgraph = fullgraph
        self.partgraph = partgraph
        self.add = []

    def run(self):
        arr = GetParamsArray(info)
        count = 0
        stop = False
        while not stop:
            stop = True
            print("Now there are " + str(len(self.add)) + " nodes")
            for node in self.partgraph:
                s = Solver()
                current = arr[0:info[0]]
                add = arr[info[0] * 2:]
                find = String('find')
                cond = []
                cond.append(z3_funcs.IsPossible(*current, *add))
                cond.append(z3_funcs.GetHyperState(*z3_funcs.NextCurrent(current, add)) == find)
                for i in self.fullgraph:
                    cond.append(find != StringVal(i))
                cond.append(z3_funcs.GetHyperState(*current) == StringVal(node))
                # cond.append(Or([z3_funcs.GetHyperState(*current) == StringVal(i) for i in graph.keys()]))
                s.add(cond)
                # solve(cond)
                if s.check() == sat:
                    stop = False
                    m = s.model()
                    add.append(str(m).split('find = ')[1].split(',')[0].strip('"'))
                    break


def UpdateNodesThreading(graph):
    threads = []
    nodes_list = list(graph.keys())
    part = 4
    step = len(nodes_list) // part

    for i in range(part - 1):
        threads.append(FindNodes(nodes_list, nodes_list[step * i : step * (i + 1)]))
    threads.append(FindNodes(nodes_list, nodes_list[step * (part - 1) :]))
    for thread in threads:
        thread.start()
    while True:
        stop = False
        for i in threads:
            stop += i.is_alive()
        if not stop:
            break
    for thread in threads:
        for node in thread.add:
            graph.add(node, [])
    return graph


def UpdateConnectionsThreading(graph):
    threads = []
    nodes_list = list(graph.keys())
    part = 2
    step = len(nodes_list) // part

    for i in range(part - 1):
        threads.append(FindEdges(graph, nodes_list[step * i: step * (i + 1)]))
    threads.append(FindEdges(graph, nodes_list[step * (part - 1):]))
    for thread in threads:
        thread.start()
    while True:
        stop = False
        for i in threads:
            stop += i.is_alive()
        if not stop:
            break
    for thread in threads:
        for node in thread.add.keys():
            graph[node] += thread.add[node]
            print(thread.add[node])
    return graph
'''
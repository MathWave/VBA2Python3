from translate import translate
from random import choice
from os import remove
from queue import *
from z3 import *
from Threading import *
from time import time
import networkx as nx
import matplotlib.pyplot as plt


amount_of_tests = 1


def GetParamsArray(info):
    arr = []
    for i in range(2 * info[0]):
        arr.append(Int('x_' + str(i) + '_int'))
    for i in range(info[1]):
        if (type(info[2 + i][0]) is int):
            arr.append(Int('x_' + str(info[0] * 2 + i + 2) + '_int'))
        else:
            arr.append(String('x_' + str(info[0] * 2 + i + 2) + '_str'))
    return arr


def getValue(model, param):
    values = str(model).replace('[', '').replace(']', '').split(',\n')
    for i in values:
        if i.__contains__(param):
            return i.split(' = ')[1].strip('"')


def UpdateConnections(graph):
    arr = GetParamsArray(info)
    count = 0
    s = Solver()
    find = String('find')
    add = arr[info[0] * 2:]
    current = arr[0:info[0]]
    s.add(z3_funcs.IsPossible(*current, *add))
    s.add([z3_funcs.NextCurrent(arr[0:info[0]], arr[info[0] * 2:])[i] == arr[info[0] + i] for i in range(info[0])])
    s.add(find == z3_funcs.GetHyperState(*arr[info[0]:info[0] * 2]))
    for node in graph.keys():
        flag = True
        while flag:
            s.push()
            s.add(z3_funcs.GetHyperState(*current) == StringVal(node))
            for node2 in graph[node]:
                s.add(z3_funcs.GetHyperState(*arr[info[0]:info[0] * 2]) != StringVal(node2))
            if s.check() == sat:
                model = str(s.model())
                graph[node].add(getValue(model, 'find'))
            else:
                flag = False
            s.pop()
        print('ready ' + str(count / len(graph.keys()) * 100) + ' %')
        count += 1
    return graph


def UpdateNodes(graph):
    arr = GetParamsArray(info)
    q = Queue()
    for i in graph.keys():
        q.put(i)
    s = Solver()
    current = arr[0:info[0]]
    add = arr[info[0] * 2:]
    find = String('find')
    s.add(z3_funcs.IsPossible(*current, *add))
    s.add(z3_funcs.GetHyperState(*z3_funcs.NextCurrent(current, add)) == find)
    while not q.empty():
        s.push()
        node = q.queue[0]
        s.add([find != StringVal(name) for name in graph.keys()])
        s.add(z3_funcs.GetHyperState(*current) == StringVal(node))
        if s.check() == sat:
            m = s.model()
            newval = getValue(m, 'find')
            graph[newval] = set()
            graph[node].add(newval)
            q.put(newval)
            print("Now there are " + str(len(graph.keys())) + " nodes")
        else:
            print("All nodes connected with " + node + " found")
            q.get()
        s.pop()
    return graph


def updateGraph(graph):
    arr = GetParamsArray(info)
    q = Queue()
    for i in graph.keys():
        q.put(i)
    s = Solver()
    current = arr[0:info[0]]
    add = arr[info[0] * 2:]
    find = String('find')
    s.add(z3_funcs.IsPossible(*current, *add))
    s.add(z3_funcs.GetHyperState(*z3_funcs.NextCurrent(current, add)) == find)
    while not q.empty():
        node = q.queue[0]
        cond = []
        cond += [find != StringVal(name) for name in graph.keys()]
        cond.append(z3_funcs.GetHyperState(*current) == StringVal(node))
        s.add(cond)
        if s.check() == sat:
            m = s.model()
            newval = getValue(m, 'find')
            graph[newval] = set()
            graph[node].add(newval)
            q.put(newval)
            print("Now there are " + str(len(graph.keys())) + " nodes")
        else:
            print("All nodes connected with " + node + " found")
            q.get()


def GenerateFile():
    newcur = open('newcur.py', 'w')  # тут создаем файл с единственной функцией
    funcs = open('transpep.py', 'r').read().split('\n')  # NextCurrent, которая возвращает следующее положение
    func_list = []  # в ячейках
    for line in funcs:
        if line.__contains__('def') and line.__contains__('Next'):
            func_list.append(line.split(' ')[1].split('(')[0])
    newcur.write('from transpep import *\n\n')
    newcur.write('def NextCurrent(current, data):\n')
    newcur.write('\treturn [')
    newcur.write(func_list[0] + '(*current, *data)')
    for f in func_list[1:]:
        newcur.write(', ' + f + '(*current, *data)')
    newcur.write(']')
    newcur.close()


def PrintArr(arr): # вывод массива
    line = ''
    for i in arr:
        line += str(i) + ' '
    return line


def FindNodeWay(graph):
    arr = GetStartPosition()
    q = Queue()
    q.put([GetHyperState(*arr)])
    last_in_queue = []
    while not q.empty():
        last_in_queue = q.get()
        last_top = last_in_queue[-1]
        for top in graph.keys():
            last_combo = last_in_queue.copy()
            if top in graph[last_top] and top not in last_in_queue:
                last_combo.append(top)
                q.put(last_combo)
                length = q.qsize()
                if length % 100000 == 0:
                    print("queue length: " + str(length))
    if len(last_in_queue) == len(list(graph.keys())):
        return last_in_queue
    else:
        q = Queue()
        q.put(last_in_queue)
        while True:
            last_in_queue = q.get()
            last_top = last_in_queue[-1]
            for top in graph.keys():
                last_combo = last_in_queue.copy()
                if top in graph[last_top]:
                    last_combo.append(top)
                    q.put(last_combo)
            if set(last_in_queue) == set(graph.keys()):
                return last_in_queue


def GetCurrentConnection(way):
    cons = []
    for i in range(len(way) - 1):
        cons.append([way[i], way[i + 1]])
    return cons


def GetInstruction(way):
    stop = False
    stop_position = 10000

    while not stop:
        current = GetStartPosition()  # текущее положение в ячейках
        answer = []
        for i in range(1, len(way)):
            count = 0
            while True:  # генерируем тестовый комплект
                data = []
                for j in more_info:
                    data.append(choice(j))
                if IsPossible(*current, *data):
                    nextcurrent = NextCurrent(current, data)
                    if GetHyperState(*nextcurrent) == way[i]:
                        answer.append(data)
                        current = nextcurrent
                        if len(way) == len(answer) + 1:
                            stop = True
                        break
                else:
                    count += 1
                if count == stop_position:
                    break
            if count == stop_position:
                break
    return answer


def FindConnectionWay(graph):
    arr = GetStartPosition()
    all_connections = []
    for key in graph.keys():
        for node in graph[key]:
            all_connections.append([key, node])
    q = Queue()
    q.put([GetHyperState(*arr)])
    last_in_queue = []
    while not q.empty():
        last_in_queue = q.get()
        last_top = last_in_queue[-1]
        current_cons = GetCurrentConnection(last_in_queue)
        for top in graph.keys():
            last_combo = last_in_queue.copy()
            if top in graph[last_top] and [last_in_queue[-1], top] not in current_cons:
                last_combo.append(top)
                q.put(last_combo)
                length = q.qsize()
                if length % 100000 == 0:
                    print("queue length: " + str(length))
    if len(GetCurrentConnection(last_in_queue)) == len(all_connections):
        return last_in_queue
    else:
        q = Queue()
        q.put(last_in_queue)
        while True:
            last_in_queue = q.get()
            last_top = last_in_queue[-1]
            for top in graph.keys():
                last_combo = last_in_queue.copy()
                if top in graph[last_top]:
                    last_combo.append(top)
                    q.put(last_combo)
            if set(GetCurrentConnection(last_in_queue)) == len(all_connections):
                return last_in_queue
    #return all_connections


def Coding(graph):
    cons = {}
    arr = list(graph.keys())
    for i in range(len(arr)):
        cons[arr[i]] = i
    return cons


def GetIntGraph(graph, cons):
    intgraph = {}
    for i in graph.keys():
        ii = cons[i]
        intgraph[ii] = []
        for j in graph[i]:
            intgraph[ii].append(cons[j])
    return intgraph


def FindNodeWayZ3(graph):
    cons = Coding(graph)
    intgraph = graph
    for i in range(len(graph.keys()), 1000):
        s = Solver()
        X = [Int('x%s' % i) for i in range(i)]
        cond1 = [Or([X[j] == i for j in range(len(X))]) for i in intgraph.keys()]
        cond2 = []
        #'''
        threads = []
        for j in range(len(X) - 1):
            threads.append(CalcNodeFirst(j, X, intgraph))
        for thread in threads:
            thread.start()
        while True:
            stop = False
            for i in threads:
                stop += i.is_alive()
            if not stop:
                break
        for j in threads:
            cond2 += j.condition
        #'''
        '''
        cond2 = [Or([And(X[i] == j, X[i + 1] == k)
                     for j in intgraph.keys() for k in intgraph[j]]) for i in range(len(X) - 1)]
        '''                                                                                                             #print("condition 2 ready for " + str(i) + " position")
        cond3 = [X[0] == 0]
        s.add(cond1 + cond2 + cond3)
        #print("for " + str(i) + " checked")
        if s.check() == sat:
            #print('\n\nway:\n')
            m = s.model()
            model_str = str(s.model()).split(',\n ')
            model_str[0] = model_str[0][1:len(model_str[0])]
            model_str[-1] = model_str[-1][0:len(model_str[-1])-1]
            row = {}
            for i in range(len(model_str)):
                #print(model_str[i])
                new_arr = model_str[i].split(' ')
                row[int(new_arr[0][1::])] = int(new_arr[2])
            new_row = []
            back_cons = {}
            for i in cons.keys():
                back_cons[cons[i]] = i
            for i in range(len(row)):
                new_row.append(back_cons[row[i]])
            return new_row


def FindConnectionWayZ3(graph):
    allconnections = []
    cons = Coding(graph)
    intgraph = GetIntGraph(graph, cons)
    for i in intgraph.keys():
        for j in intgraph[i]:
            allconnections.append([i, j])
    for i in range(len(graph.keys()), 10):
        s = Solver()
        X = [Int('x%s' % j) for j in range(i)]
        cond1 = [X[0] == 0]
        cond2 = []
        threads = []
        for j in allconnections:
            threads.append(CalcEilerFirst(j, X, intgraph))
        for thread in threads:
            thread.start()
        while True:
            stop = False
            for t in threads:
                stop += t.is_alive()
            if not stop:
                break
        for j in threads:
            cond2 += j.condition
        print("thread for " + str(i) + " created")
        s.add(cond1 + cond2)
        if s.check() == sat:
            # print('\n\nway:\n')
            m = s.model()
            model_str = str(s.model()).split(',\n ')
            model_str[0] = model_str[0][1:len(model_str[0])]
            model_str[-1] = model_str[-1][0:len(model_str[-1]) - 1]
            row = {}
            for i in range(len(model_str)):
                # print(model_str[i])
                new_arr = model_str[i].split(' ')
                row[int(new_arr[0][1::])] = int(new_arr[2])
            new_row = []
            back_cons = {}
            for i in cons.keys():
                back_cons[cons[i]] = i
            for i in range(len(row)):
                new_row.append(back_cons[row[i]])
            return new_row


def BuildGraph(n):
    current = GetStartPosition()
    connections = {}

    for i in range(n):  # сколько тестов генерируем
        while True:  # генерируем тестовый комплект
            data = []
            for j in more_info:
                data.append(choice(j))
            if IsPossible(*current, *data):
                break
        nextcurrent = NextCurrent(current, data)  # получаем следующее значение в ячейках
        if GetHyperState(*current) not in list(connections.keys()):  # если позиция ячеек еще не встречалась, добавляем
            connections[GetHyperState(*current)] = set()  # ее в словарь
        connections[GetHyperState(*current)].add(GetHyperState(*nextcurrent))  # добавляем связь
        current = nextcurrent
        print(str(i + 1) + ": " + PrintArr(data) + '\t\t' + GetHyperState(*current) + '\t\t' + PrintArr(current))
        res.write('"' + str(i + 1) + '";"' + PrintArr(data) + '";"' + GetHyperState(*current) + '";"' + PrintArr(
            current) + '"\n')
        # выводим результат в консоль и записываем в csv
        if StopCondition(*current):
            current = GetStartPosition()
    return connections


def node_amount(graph):
    return len(graph.keys())


def connections_amount(graph):
    sum = 0
    for i in graph.keys():
        sum += len(graph[i])
    return sum


def printGraph(graph):
    for i in graph:
        print(str(i) + ": " + str(graph[i]))



translate("code.txt") # переводим код, он записывается в transpep

import transpep
from transpep import * # импортируем файл

info = GetInfo() # информация по обрабатываемым функциям

more_info = []
for i in range(info[1] + 2):
    more_info.append(info[i])
more_info = more_info[2:]

res = open('results.csv', 'w')

GenerateFile()

from newcur import NextCurrent

#graph = BuildIntGraph(100000)

#for con in graph.keys():
#    graph[con] = list(set(graph[con]))


connections = BuildGraph(amount_of_tests)

print('\n\n\n')

printGraph(connections)

res.close()
#remove('trans.py')        # удаляем сгенерированные файлы
#remove('transpep.py')
#remove('newcur.py')

nodes = set(connections.keys())

'''

print("\n\nNode way:")
way = FindNodeWay(connections)
print(way)

print('\nInstructions: ')

answer = GetInstruction(way)

for i in answer:
    print(i)

print('\n\nEuler:\n\n')



ans = FindConnectionWay(connections)
for i in ans:
    print(i)
'''
#print(FindConnectionWay(connections))

print("HAPPYEND!!!!")

print("\n\nIn current graph:\n" + str(node_amount(connections)) + " nodes\n" + str(connections_amount(connections)) + " connections\n\n")

print("Updating...\n\n")

from Z3Translator import create_z3

create_z3()

import z3_funcs

t = time()
connections = UpdateNodes(connections)
print('\n\nSpent time for nodes: ' + str(int(time() - t)))
connections = UpdateConnections(connections)
print('\n\nSpent time for all: ' + str(int(time() - t)))

print("\n\nNow there are \n" + str(node_amount(connections)) + " nodes\n" + str(connections_amount(connections)) + " connections\n\n")

printGraph(connections)

print("HAPPYEND!!!![2]")

G = nx.DiGraph()

for node in connections.keys():
    for node2 in connections[node]:
        G.add_edge(node, node2)

nx.draw(G, with_labels=True, font_weight='bold')

plt.show()

'''
print("\n\nNode way:")
way = FindNodeWay(connections)
print(way)

print('\nInstructions: ')

answer = GetInstruction(way)

for i in answer:
    print(i)
'''

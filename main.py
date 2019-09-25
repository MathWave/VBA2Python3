from translate import translate
from random import choice
from os import remove
from queue import *
from z3 import *

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


def GetStartPosition():
    global info
    arr = []
    for top in range(info[0]):
        arr.append(0)
    return arr


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


def ReverseGraph(graph):
    newgraph = {}
    for i in graph.keys():
        for j in graph[i]:
            if j not in newgraph.keys():
                newgraph[j] = [i]
            else:
                newgraph[j].append(i)
    return newgraph


def FindNodeWayZ3(graph):
    intgraph = {}
    cons = {}
    arr = list(graph.keys())
    for i in range(len(arr)):
        cons[arr[i]] = i
    for i in graph.keys():
        ii = cons[i]
        intgraph[ii] = []
        for j in graph[i]:
            intgraph[ii].append(cons[j]);
    for i in range(len(graph.keys()), 1000):
        s = Solver()
        X = [Int('x%s' % i) for i in range(i)]
        cond1 = [Or([X[j] == i for j in range(len(X))]) for i in intgraph.keys()]
        print("condition 1 ready for " + str(i) + " position")
        cond2 = [Or([And(X[i] == j, X[i + 1] == k) for j in intgraph.keys() for k in intgraph[j]]) for i in range(len(X) - 1)]
        print("condition 2 ready for " + str(i) + " position")
        cond3 = [X[0] == 0]
        s.add(cond1 + cond2 + cond3)
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


translate("code.txt") # переводим код, он записывается в transpep

import transpep
from transpep import * # импортируем файл

info = GetInfo() # информация по обрабатываемым функциям
current = [] # текущее положение в ячейках

for i in range(info[0]):
    current.append(0)

more_info = []
for i in range(info[1] + 2):
    more_info.append(info[i])
more_info = more_info[2:]

res = open('results.csv', 'w')

GenerateFile()

from newcur import NextCurrent

connections = {}

for i in range(100000): # сколько тестов генерируем
    while True: # генерируем тестовый комплект
        data = []
        for j in more_info:
            data.append(choice(j))
        if IsPossible(*current, *data):
            break
    nextcurrent = NextCurrent(current, data) # получаем следующее значение в ячейках
    if GetHyperState(*current) not in list(connections.keys()): # если позиция ячеек еще не встречалась, добавляем
        connections[GetHyperState(*current)] = []               # ее в словарь
    connections[GetHyperState(*current)].append(GetHyperState(*nextcurrent)) # добавляем связь
    current = nextcurrent
    print(str(i + 1) + ": " + PrintArr(data) + '\t\t' + GetHyperState(*current) + '\t\t' + PrintArr(current))
    res.write('"' + str(i + 1) + '";"' + PrintArr(data) + '";"' + GetHyperState(*current) + '";"' + PrintArr(current) + '"\n')
    # выводим результат в консоль и записываем в csv

for con in connections.keys():
    connections[con] = set(connections[con])

print('\n\n\n')

for con in connections.keys():                       # выводим ребра графа в консоль
    print(str(con) + ": " + str(connections[con]))
res.close()
remove('trans.py')        # удаляем сгенерированные файлы
remove('transpep.py')
remove('newcur.py')

nodes = set(connections.keys())

print("\n\nZ3:\n\n")
print(FindNodeWayZ3(connections))

print("\n\nThe way:")
way = FindNodeWay(connections)
print(way)

'''

print('\nInstructions: ')

stop = False
stop_position = 10000

while not stop:
    current = GetStartPosition()  # текущее положение в ячейках
    answer = []
    for i in range(1, len(way)):
        count = 0
        while True: # генерируем тестовый комплект
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

for i in answer:
    print(i)

print('new: ')
print(FindConnectionWay(connections))

print("HAPPYEND!!!!")
'''
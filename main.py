from translate import translate
from random import choice
from os import remove, rmdir
from queue import *
from z3 import *
from time import time
import networkx as nx
import matplotlib.pyplot as plt
from zipfile import ZipFile
import subprocess
import os
from xlwt import Workbook

###################################### MAIN CONTROLLERS ################################################################

try:
    openfile = sys.argv[2]
    saveto = sys.argv[3] + '/' + sys.argv[4]
    amount_of_tests = int(sys.argv[5])
    area = True if sys.argv[6] == 'True' else False
except:
    log = open('logs.txt', 'w')
    log.write("Error in input information!")
    log.close()
    exit(1)

########################################################################################################################

def deletePythonFiles():
    remove('trans.py')        # удаляем сгенерированные файлы
    remove('transpep.py')
    remove('newcur.py')


def DeleteAll():
    remove('z3_funcs.py')
    for root, dirs, files in os.walk('here', topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir('here')


def deleteVBA():
    remove('code.txt')


def takeVBA(pathfrom, pathto):
    with ZipFile(pathfrom, 'r') as zipObj:
        zipObj.extractall('here')
    pathfrom = './here/xl/vbaProject.bin'
    python3_command = "python2 ./oledump/oledump.py -f " + pathfrom + " -t " + pathto + ""  # launch your python2 script using bash
    subprocess.run(python3_command.split())


def getValue(model, param):
    values = str(model).replace('[', '').replace(']', '').split(',\n')
    for i in values:
        if i.__contains__(param):
            return i.split(' = ')[1].strip('"')
    num = int(param.split('_')[1])
    return choice(info[num + 2 - 2 * info[0]])




def getHyperStateZ3(model, info):
    return GetHyperState(*[int(getValue(model, 'x_' + str(i) + '_int')) for i in range(info[0], info[0] * 2)])


def GetParamsArray(info):
    arr = []
    for i in range(2 * info[0]):
        arr.append(Int('x_' + str(i) + '_int'))
    for i in range(info[1]):
        if type(info[2 + i][0]) is int:
            arr.append(Int('x_' + str(info[0] * 2 + i) + '_int'))
        else:
            arr.append(String('x_' + str(info[0] * 2 + i) + '_str'))
    return arr


def GetNewTouple(model, info):
    arr = GetParamsArray(info)
    newarr = []
    for i in arr:
        newarr.append(getValue(model, str(i)))
    return [PrintArr(newarr[0:info[0]]), PrintArr(newarr[info[0]*2:]), PrintArr(newarr[info[0]:info[0]*2])]



def UpdateConnections(graph):
    arr = GetParamsArray(info)
    count = 0
    s = Solver()
    add = arr[info[0] * 2:]
    current = arr[0:info[0]]
    s.add(z3_funcs.IsPossible(*current, *add))
    s.add([z3_funcs.NextCurrent(arr[0:info[0]], arr[info[0] * 2:])[i] == arr[info[0] + i] for i in range(info[0])])
    for node in graph.keys():
        flag = True
        while flag:
            s.push()
            s.add(z3_funcs.GetHyperState(*current) == StringVal(node))
            for node2 in graph[node]:
                s.add(z3_funcs.GetHyperState(*arr[info[0]:info[0] * 2]) != StringVal(node2))
            if s.check() == sat:
                model = str(s.model())
                graph[node].add(getHyperStateZ3(model, info))
                examples.append(GetNewTouple(model, info))
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
    nextcur = arr[info[0]:info[0] * 2]
    add = arr[info[0] * 2:]
    find = String('find')
    s.add(z3_funcs.IsPossible(*current, *add))
    s.add([z3_funcs.NextCurrent(arr[0:info[0]], arr[info[0] * 2:])[i] == arr[info[0] + i] for i in range(info[0])])
    s.add(find == z3_funcs.GetHyperState(*nextcur))
    while not q.empty():
        s.push()
        node = q.queue[0]
        s.add([find != StringVal(name) for name in graph.keys()])
        s.add(z3_funcs.GetHyperState(*current) == StringVal(node))
        if s.check() == sat:
            m = str(s.model())
            newval = getValue(m, 'find')
            graph[newval] = set()
            examples.append(GetNewTouple(m, info))
            graph[node].add(newval)
            q.put(newval)
            print("Now there are " + str(len(graph.keys())) + " nodes")

        else:
            print("All nodes connected with " + node + " found")
            q.get()
        s.pop()
        if area:
            s.push()
            s.add(z3_funcs.GetHyperState(*nextcur) == StringVal(node))
            get = String('get')
            s.add(get == z3_funcs.GetHyperState(*current))
            s.add([get != StringVal(line) for line in graph.keys()])
            if s.check() == sat:
                m = str(s.model())
                newval = getValue(m, 'get')
                graph[newval] = set()
                graph[newval].add(getValue(m, 'find'))
                examples.append(GetNewTouple(m, info))
                q.put(newval)
                print("Now there are " + str(len(graph.keys())) + " nodes")
            s.pop()


    return graph


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
    return line[0:len(line)-1]


def BuildGraph(n, wb):
    res = open('results.csv', 'w')
    current = GetStartPosition()
    connections = {}
    rnd = wb.add_sheet('Random Testing')
    rnd.write(0, 0, '№')
    rnd.write(0, 1, 'Current')
    rnd.write(0, 2, 'Current Hyperstate')
    rnd.write(0, 3, 'Addition')
    rnd.write(0, 4, 'Next')
    rnd.write(0, 5, 'Next Hyperstate')
    for i in range(n):  # сколько тестов генерируем
        while True:  # генерируем тестовый комплект
            data = []
            for j in more_info:
                data.append(choice(j))
            if IsPossible(*current, *data):
                break
        cur_hyper = GetHyperState(*current)
        nextcurrent = NextCurrent(current, data)  # получаем следующее значение в ячейках
        next_hyper = GetHyperState(*nextcurrent)
        if cur_hyper not in list(connections.keys()):  # если позиция ячеек еще не встречалась, добавляем
            connections[cur_hyper] = set()  # ее в словарь
        if next_hyper not in connections[cur_hyper]:
            connections[cur_hyper].add(next_hyper)  # добавляем связь
            examples.append([PrintArr(current), PrintArr(data), PrintArr(nextcurrent)])
        if i < 65535:
            rnd.write(i + 1, 0, i + 1)
            rnd.write(i + 1, 1, PrintArr(current))
            rnd.write(i + 1, 2, GetHyperState(*current))
            rnd.write(i + 1, 3, PrintArr(data))
            rnd.write(i + 1, 4, PrintArr(nextcurrent))
            rnd.write(i + 1, 5, GetHyperState(*nextcurrent))
        current = nextcurrent
        print(str(i + 1) + ": " + PrintArr(data) + '\t\t' + GetHyperState(*current) + '\t\t' + PrintArr(current))
        res.write('"' + str(i + 1) + '";"' + PrintArr(data) + '";"' + GetHyperState(*current) + '";"' + PrintArr(
            current) + '"\n')
        # выводим результат в консоль и записываем в csv
        if StopCondition(*current):
            current = GetStartPosition()
    res.close()
    return connections


def node_amount(graph):
    return len(graph.keys())


def connections_amount(graph):
    sum = 0
    for i in graph.keys():
        sum += len(graph[i])
    return sum


def printGraph(graph, wb):
    rnd = wb.add_sheet('Graph of Hyperstates')
    rnd.write(0, 0, 'Node')
    rnd.write(0, 1, 'Nexts')
    nodes = list(graph.keys())
    for i in range(len(nodes)):
        rnd.write(i + 1, 0, nodes[i])
        l = list(graph[nodes[i]])
        for j in range(len(l)):
            rnd.write(i + 1, j + 1, l[j])
    # for i in graph:
    #     print(str(i) + ": " + str(graph[i]))


def ExamplesOutput(wb):
    rnd = wb.add_sheet('Instructions')
    rnd.write(0, 0, 'Before')
    rnd.write(0, 1, 'Add')
    rnd.write(0, 2, 'After')
    for i in range(len(examples)):
        for j in range(3):
            rnd.write(i + 1, j, examples[i][j])


########################################################################################################################

try:
    wb = Workbook()

    examples = []

    takeVBA(openfile, 'code.txt')

    translate("code.txt") # переводим код, он записывается в transpep

    deleteVBA()

    import transpep
    from transpep import * # импортируем файл

    info = GetInfo() # информация по обрабатываемым функциям

    more_info = []
    for i in range(info[1] + 2):
        more_info.append(info[i])
    more_info = more_info[2:]

    GenerateFile()

    from newcur import NextCurrent

    connections = BuildGraph(amount_of_tests, wb)

    #print('\n\n\n')

    #printGraph(connections, wb)

    # print("HAPPYEND!!!!")
    #
    # print("\n\nIn current graph:\n" + str(node_amount(connections)) + " nodes\n" + str(connections_amount(connections)) + " connections\n\n")
    #
    # print("Updating...\n\n")

    from Z3Translator import create_z3

    create_z3()

    deletePythonFiles()

    import z3_funcs

    t = time()
    connections = UpdateNodes(connections)
    #print('\n\nSpent time for nodes: ' + str(int(time() - t)))
    connections = UpdateConnections(connections)

    DeleteAll()

    print('\n\nSpent time for all: ' + str(int(time() - t)))

    print("\n\nNow there are \n" + str(node_amount(connections)) + " nodes\n" + str(connections_amount(connections)) + " connections\n\n")

    printGraph(connections, wb)

    #print("HAPPYEND!!!![2]")

    ExamplesOutput(wb)

    wb.save(saveto)

    # G = nx.DiGraph()
    #
    # for node in connections.keys():
    #     for node2 in connections[node]:
    #         G.add_edge(node, node2)
    #
    # nx.draw(G, font_weight='bold', with_labels=False, width=0.5)
    #
    # plt.show()

except Exception as e:
    log = open('logs.txt', 'w')
    log.write(str(e))
    log.close()
    exit(1)

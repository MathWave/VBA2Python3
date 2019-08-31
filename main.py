from translate import translate
from random import choice
from os import remove

def PrintArr(arr):
    line = ''
    for i in arr:
        line += str(i) + ' '
    return line

translate("code.txt")

import transpep
from transpep import *

info = GetInfo()
current = []

for i in range(info[0]):
    current.append(0)

more_info = []
for i in range(info[1] + 2):
    more_info.append(info[i])
more_info = more_info[2:]

res = open('results.csv', 'w')

connections = {}

for i in range(100000):
    while True:
        data = []
        for j in more_info:
            data.append(choice(j))
        if IsPossible(*current, *data):
            break
    new_current = []
    newcur = open('newcur.py', 'w')
    funcs = open('transpep.py', 'r').read().split('\n')
    func_list = []
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
    from newcur import NextCurrent
    nextcurrent = NextCurrent(current, data)
    kkk = list(connections.keys())
    if GetHyperState(*current) not in list(connections.keys()):
        connections[GetHyperState(*current)] = []
    connections[GetHyperState(*current)].append(GetHyperState(*nextcurrent))
    current = nextcurrent
    print(str(i + 1) + ": " + PrintArr(data) + '\t\t' + GetHyperState(*current) + '\t\t' + PrintArr(current))
    res.write('"' + str(i + 1) + '";"' + PrintArr(data) + '";"' + GetHyperState(*current) + '";"' + PrintArr(current) + '"\n')

for con in connections.keys():
    connections[con] = list(set(connections[con]))

print('\n\n\n')

for con in connections.keys():
    print(str(con) + ": " + str(connections[con]))
res.close()
remove('trans.py')
remove('transpep.py')
remove('newcur.py')

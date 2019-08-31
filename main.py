from translate import translate
from random import choice
from os import remove

def PrintArr(arr): # вывод массива
    line = ''
    for i in arr:
        line += str(i) + ' '
    return line

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

newcur = open('newcur.py', 'w')                                   # тут создаем файл с единственной функцией
funcs = open('transpep.py', 'r').read().split('\n')               # NextCurrent, которая возвращает следующее положение
func_list = []                                                    # в ячейках
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

connections = {}

for i in range(100000): # сколько тестов генерируем
    while True: # генерируем тестовый комплект
        data = []
        for j in more_info:
            data.append(choice(j))
        if IsPossible(*current, *data):
            break
    new_current = []
    nextcurrent = NextCurrent(current, data) # получаем следующее значение в ячейках
    if GetHyperState(*current) not in list(connections.keys()): # если позиция ячеек еще не встречалась, добавляем
        connections[GetHyperState(*current)] = []               # ее в словарь
    connections[GetHyperState(*current)].append(GetHyperState(*nextcurrent)) # добавляем связь
    current = nextcurrent
    print(str(i + 1) + ": " + PrintArr(data) + '\t\t' + GetHyperState(*current) + '\t\t' + PrintArr(current))
    res.write('"' + str(i + 1) + '";"' + PrintArr(data) + '";"' + GetHyperState(*current) + '";"' + PrintArr(current) + '"\n')
    # выводим результат в консоль и записываем в csv

for con in connections.keys():
    connections[con] = list(set(connections[con]))

print('\n\n\n')

for con in connections.keys():                       # выводим ребра графа в консоль
    print(str(con) + ": " + str(connections[con]))
res.close()
remove('trans.py')        # удаляем сгенерированные файлы
remove('transpep.py')
remove('newcur.py')

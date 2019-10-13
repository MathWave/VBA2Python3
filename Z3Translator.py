from z3 import *
from z3_funcs import *

def find_strings(line):
    instring = False
    buffer = ""
    string_arr = []
    for i in line:
        if i == '"':
            instring ^= True
            if not instring:
                string_arr.append(buffer[1::])
                buffer = ""
        if instring:
            buffer += i
    return set(string_arr)


def from_array_into_string(arr):
    line = ""
    for i in arr:
        line += i + ', '
    return line[0:len(line) - 2]


def make_operands(line):
    arr = line.split(', ')
    newline = line
    for elem in arr:
        if elem.__contains__(' or '):
            oper = elem.split('If(')[1]
            and_args = oper.split(' or ')
            newl = 'Or(' + from_array_into_string(and_args) + ')'
            newline = newline.replace(oper, newl)
    arr = newline.split(', ')
    for elem in arr:
        if elem.__contains__(' and '):
            if elem.__contains__('Or('):
                oper = elem.split('Or(')[1]
            elif elem.__contains__('If('):
                oper = elem.split('If(')[1]
            else:
                oper = elem
            and_args = oper.split(' and ')
            newl = 'And(' + from_array_into_string(and_args) + ')'
            newline = newline.replace(oper, newl)
    #return line
    return newline


def create_z3():
    z3_funcs = open('z3_funcs.py', 'w')
    original = open('transpep.py', 'r')
    z3_funcs.write("from z3 import *\n\n")
    def_list = []
    buffer = ""
    there_was_if_before = False
    recursion_level = 0
    for line in original:
        if line.__contains__('def'):
            z3_funcs.write('\n\n' + line)
            def_list.append(line.split(' ')[1].split('(')[0])
            buffer = "\treturn "
        elif line.__contains__('if'):
            if not line.__contains__('elif'):
                recursion_level += 1
            buffer += 'If(' + line.split('if')[1].split(':')[0].strip() + ', '
            there_was_if_before = True
        elif line.__contains__('else'):
            recursion_level -= 1
            there_was_if_before = False
        elif line.__contains__('return'):
            buffer += line.split('return')[1].strip()
            if there_was_if_before:
                buffer += ', '
            else:
                buffer += '), '
            if recursion_level == 0:
                newbuf = buffer[0:len(buffer) - 2]
                left = 0
                right = 0
                for i in newbuf:
                    if i == '(':
                        left += 1
                    elif i == ')':
                        right += 1
                if left > right:
                    for i in range(left - right):
                        newbuf += ')'
                else:
                    for i in range(right - left):
                        newbuf = newbuf[0:len(newbuf) - 1]
                strings = find_strings(newbuf)
                for string in strings:
                    newbuf = newbuf.replace('"' + string + '"', 'StringVal("' + string + '")')
                newbuf = make_operands(newbuf)
                z3_funcs.write(newbuf)
                buffer = "\treturn "


    #print(def_list)
    newcur = open('newcur.py').read().split('\n')
    z3_funcs.write('\n\n' + newcur[2] + '\n')
    z3_funcs.write(newcur[3])
    z3_funcs.close()
    return def_list


def UpdateGraph(graph, info):
    create_z3()
    arr = []
    for i in range(2 * info[0]):
        arr.append(Int('x_' + str(i)))
    for i in range(info[1]):
        if (type(info[2 + i][0]) is int):
            arr.append(Int('x_' + str(info[0] * 2 + i + 2)))
        else:
            arr.append(String('x_' + str(info[0] * 2 + i + 2)))
    for node in graph:
        for node2 in graph:
            if node2 not in graph[node]:
                s = Solver()
                cond = []
                cond.append(GetHyperState(*arr[0:info[0]]) == StringVal(node))
                cond.append(GetHyperState(*arr[info[0]:info[0] * 2]) == StringVal(node2))
                for i in range(info[0]):
                    cond.append(NextCurrent(arr[0:info[0]], arr[info[0] * 2:info[0] * 2 + info[1]])[i] == arr[info[0] + i])
                s.add(cond)
                if s.check() == sat:
                    graph[node].append(node2)
    return graph


create_z3()
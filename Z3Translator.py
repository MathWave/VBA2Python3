from Stack import Stack


def pop_condition(s):
    if s.size() < 4:
        return False
    if s.index(0).__contains__('return') and s.index(1).__contains__('else') and s.index(2).__contains__('return') and s.index(3).__contains__('if'):
        return True
    return False


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


def improve_line(line):
    newbuf = '\t' + line
    strings = find_strings(newbuf)
    for string in strings:
        newbuf = newbuf.replace('"' + string + '"', 'StringVal("' + string + '")')
    newbuf = make_operands(newbuf)
    return newbuf


def create_z3():
    z3_funcs = open('z3_funcs.py', 'w')
    original = open('transpep.py', 'r')
    z3_funcs.write("from z3 import *\n\n")
    s = Stack()
    for line in original:
        line = line.replace('\n', '')
        if line.__contains__('def '):
            if not s.isEmpty():
                z3_funcs.write(improve_line(s.pop()))
            z3_funcs.write('\n\n' + line + '\n')
        elif line.__contains__('elif '):
            s.push('else')
            s.push('if ' + line.split('elif ')[1].split(':')[0])
        elif line.__contains__('if '):
            s.push('if ' + line.split('if ')[1].split(':')[0])
        elif line.__contains__('else'):
            s.push('else')
        elif line.__contains__('return '):
            s.push('return ' + line.split('return ')[1])
        while pop_condition(s):
            a = s.pop()
            b = s.pop()
            c = s.pop()
            d = s.pop()
            s.push("return If(" + d[3:] + ', ' + c[7:] + ', ' + a[7:] + ')')
    z3_funcs.write(improve_line(s.pop()))
    newcur = open('newcur.py').read().split('\n')
    z3_funcs.write('\n\n' + newcur[2] + '\n')
    z3_funcs.write(newcur[3])
    z3_funcs.close()


#create_z3()
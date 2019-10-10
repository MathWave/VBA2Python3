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
                z3_funcs.write(newbuf)
                buffer = "\treturn "


    print(def_list)
    z3_funcs.close()


create_z3()
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
            z3_funcs.write(line)
            def_list.append(line.split(' ')[1].split('(')[0])
            buffer = "\treturn "
        elif line.__contains__('if'):
            recursion_level += 1
            buffer += 'If(' + line.split('if')[1].split(':')[0].strip() + ', '
            there_was_if_before = True
        elif line.__contains__('else'):
            recursion_level -= 1
            there_was_if_before = False
            pass
        elif line.__contains__('return'):
            buffer += line.split('return')[1].strip()
            if there_was_if_before:
                buffer+= ', '
            else:
                buffer += ')'
            if recursion_level == 0:
                z3_funcs.write(buffer)
                buffer = "\treturn "


    print(def_list)
    z3_funcs.close()
import autopep8

def MakeOperands(line): # перевод логических операций
    newline = line.replace(' And ', ' and ')\
        .replace(' Or ', ' or ')
    newl = ''
    for i in range(len(newline)): # а тут исправляем <= и >=
        if newline[i] == '=':
            if newline[i-1] == '<' or newline[i-1] == '>' or newline[i+1] == '<' or newline[i+1] == '>':
                newl += '='
            else:
                newl += '=='
        else:
            newl += newline[i]
    return newl.replace('<>', '!=')

def translate(filename):
    file = open(filename, 'r').read()\
        .replace(' Then', ':')\
        .replace('End If', '')\
        .replace('CStr', 'str')\
        .split('\n') # переводим некоторые функции, не требующие дополнительного вмешательства
    trans = open("trans.py", 'w')

    current = ""

    for line in file: # тут простой перевод
        if line.__contains__('End Function'):
            trans.write('\n')
            current = ''
        elif line.__contains__('Function'):
            trans.write(line.replace('Function', 'def') + ':' + '\n')
            current = line.split(' ')[1].split('(')[0]
        elif line.__contains__("'"):
            trans.write(line.replace("'", '#') + '\n')
        elif line.__contains__('ElseIf'):
            trans.write(MakeOperands(line.replace('ElseIf', 'elif')) + '\n')
        elif line.__contains__("If"):
            trans.write(MakeOperands(line.replace("If", 'if')) + '\n')
        elif line.__contains__("Else"):
            kek = MakeOperands(line.replace("Else", 'else')) + ':' + '\n'
            trans.write(MakeOperands(line.replace("Else", 'else').replace(':', '')) + ':' + '\n')
        elif line.__contains__(current):
            if line.__contains__('&'): # конкатинация строк
                if current == 'GetHyperState':
                    line = line.replace('&', '+')
            if line.__contains__('Array'):
                line = line.replace('Array(', '[').replace(')', ']')
            trans.write(line.replace(current + ' =', 'return') + '\n')
        elif line.__contains__('&'):
            if current == 'GetHyperState':
                trans.write(line.replace('&', '+') + '\n')
        else:
            trans.write(line + '\n')
    trans.close()
    lll = autopep8.fix_file('trans.py') # приводим код к pep8
    fff = open('transpep.py', 'w')
    fff.write(lll)
    fff.close()
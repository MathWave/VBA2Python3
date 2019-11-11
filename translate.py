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


def __solveBracketsInArray__(line):
    conflicts = []
    i = 0
    newline = ''
    while i < len(line):
        if line[i:i+5] == 'Array':
            newline += '['
            i += 6
            conflicts.append(1)
            continue
        if line[i] == '(':
            conflicts[-1] += 1
            newline += '('
        elif line[i] == ')':
            conflicts[-1] -= 1
            if conflicts[-1] == 0:
                newline += ']'
                conflicts.pop(-1)
            else:
                newline += ')'
        else:
            newline += line[i]
        i += 1
    return newline



def translate(filename):
    file = open(filename, 'r').read()\
        .replace(' Then', ':')\
        .replace('End If', '')\
        .replace('CStr', 'str')\
        .replace(' Mod ', ' % ')

    trans = open("trans.py", 'w')
    if file.__contains__('Rnd'):
        trans.write("from random import randrange\n\n")
    file = file.replace('Rnd', 'randrange').split('\n') # переводим некоторые функции, не требующие дополнительного вмешательства
    current = ""

    for line in file: # тут простой перевод
        line = line.replace(' And ', ' and ').replace(' Or ', ' or ')
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
                line = __solveBracketsInArray__(line)
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
from z3 import *
from BitVector import *


def hyperstate(val, x, y):
    bv = BitVector(size=5, intVal = val)
    res = True
    for i in range(5):
        if bv[i] == 0 :
            res = And( Not(Cond[i](x,y)), res)
        else:
            res = And( Cond[i](x,y), res)
    res = simplify(res)
    return res


a_0 = z3.Int('a_0')
b_0 = z3.Int('b_0')

a_1 = z3.Int('a_1')
b_1 = z3.Int('b_1')

a = z3.Int('a')
b = z3.Int('b')
s = z3.Solver()

Cond1 = z3.Function('Cond1', IntSort(), IntSort(), BoolSort())
s.add(ForAll([a, b], Cond1(a, b) == (a > b)))

Cond2 = Function('Cond2', IntSort(), IntSort(), BoolSort())
s.add(ForAll([a, b], Cond2(a, b) == (a < 10)))

Cond3 = Function('Cond3', IntSort(), IntSort(), BoolSort())
s.add(ForAll([a, b], Cond3(a, b) == (b < 10)))

Cond4 = Function('Cond4', IntSort(), IntSort(), BoolSort())
s.add(ForAll([a, b], Cond4(a, b) == (b < a + a)))

Cond5 = Function('Cond5', IntSort(), IntSort(), BoolSort())
s.add(ForAll([a, b], Cond5(a, b) == (a < b + b)))

Cond = [Cond1, Cond2, Cond3, Cond4, Cond5]

res_file = open('res.txt', 'w')

Rule1 = If(a_0 > b_0, a_1 == a_0 - b_0, a_1 == a_0)
Rule2 = If(a_0 > b_0, b_1 == b_0, b_1 == a_0 - b_0)
s.add(Rule1, Rule2)
for i in range(1, 32):
    for j in range(1, 32):
        s.push()
        s.add(hyperstate(i, a_0, b_0), hyperstate(j, a_1, b_1))
        if str(s.check()) == 'sat':
            print('i =', i, ' j =', j)
            res_file.write( str(i) + '\t' + str(j) + '\t: ')
            res_file.write('a_0=' + str(s.model().eval(a_0)) + ' b_0=' + str(s.model().eval(b_0)) + '\n')
        s.pop()

res_file.close()

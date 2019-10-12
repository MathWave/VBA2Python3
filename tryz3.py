from z3 import *

graph = {
    "0" : ["5"],
    "1" : ["6"],
    "2" : ["7"],
    "3" : ["8"],
    "4" : ["9"],
    "5" : []
}

def HS(s):
    return

def func_z3(n):
    return If(n < 10, StringVal("less"), StringVal("more"))

def func(n):
    if n < 10:
        return "less"
    return "more"

x = String('x')
y = String('y')

cond = [And(x == StringVal('a'), y == StringVal('b'))]

solve(cond)

#cond = If(x < y, StringVal("hello"), StringVal("world"))
#f = Function('f', IntSort(), IntSort(), StringSort())
#solve(f(x,y) == cond)
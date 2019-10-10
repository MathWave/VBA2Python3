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

x = Int('x')
y = Int('y')

solve([x > 0, ])
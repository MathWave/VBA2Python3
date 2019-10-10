from z3 import *



def Next(a, b):
	return If(a < b, 1, 0)

def Add(a, b, c):
	return If(a < b, 2, If(b < c, 1, 0))
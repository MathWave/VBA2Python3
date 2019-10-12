from z3 import *



def NextBuy03(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), Buy03, If(And(Operation == StringVal("Buy"), Price == 102), If(Buy02 != 0, Volume, Buy03), If(And(Operation == StringVal("Sell"), Price == 101), If(Volume >= Buy01 + Buy11, 0, Buy03), If(Buy01 == 0, Buy03, If(Volume >= Buy01, 0, Buy03)))))

def NextBuy02(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), Buy02, If(And(Operation == StringVal("Buy"), Price == 102), If(Buy01 == 0, 0, If(Buy02 != 0, Buy02, Volume), If(And(Operation == StringVal("Sell"), Price == 101), If(Volume < Buy01 + Buy11, Buy02, If(Volume < Buy01 + Buy02 + Buy11 + Buy12, Buy03, 0), If(Buy02 == 0, 0, If(Volume < Buy01, Buy02, If(Volume < Buy01 + Buy02, Buy03, 0))))))))

def NextBuy01(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), Buy01, If(And(Operation == StringVal("Buy"), Price == 102), If(Buy01 == 0, If(Sell01 + Sell11 == 0, Volume, If(Sell02 + Sell12 == 0, If(Volume > Sell01 + Sell11, Volume - Sell01 - Sell11, 0), If(Sell03 + Sell13 == 0, If(Volume > Sell01 + Sell11 + Sell02 + Sell12, Volume - Sell01 - Sell11 - Sell02 - Sell12, 0), If(Volume > Sell01 + Sell02 + Sell03 + Sell11 + Sell12 + Sell13, Volume - Sell01 - Sell02 - Sell03 - Sell11 - Sell12 - Sell13, 0), Buy01), If(And(Operation == StringVal("Sell"), Price == 101), If(Buy01 == 0, 0, If(Buy02 == 0, If(Volume >= Buy01, 0, Buy01 - Volume), If(Buy03 == 0, If(Volume < Buy01, Buy01 - Volume, If(Volume < Buy01 + Buy02, Buy01 + Buy02 - Volume, 0), If(Volume < Buy01, Buy01 - Volume, If(Volume < Buy01 + Buy02, Buy01 + Buy02 - Volume, If(Volume < Buy01 + Buy02 + Buy03, Buy01 + Buy02 + Buy03 - Volume, 0), If(Buy01 == 0, 0, If(Buy02 == 0, If(Volume >= Buy01, 0, Buy01 - Volume), If(Buy03 == 0, If(Volume < Buy01, Buy01 - Volume, If(Volume < Buy01 + Buy02, Buy01 + Buy02 - Volume, 0), If(Volume < Buy01, Buy01 - Volume, If(Volume < Buy01 + Buy02, Buy01 + Buy02 - Volume, If(Volume < Buy01 + Buy02 + Buy03, Buy01 + Buy02 + Buy03 - Volume, 0)))))))))))))))))))

def NextSell01(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), If(Sell01 != 0, Sell01, If(Sell02 != 0, If(Volume < Sell11, Sell01, Sell02), If(Sell03 != 0, If(Volume < Sell11, Sell01, If(Volume < Sell11 + Sell12, Sell02, Sell03), 0), If(And(Operation == StringVal("Buy"), Price == 102), If(Volume < Sell01 + Sell11, If(Sell01 == 0, 0, Sell01 + Sell11 - Volume), If(Volume < Sell01 + Sell11 + Sell02 + Sell12, If(Sell02 == 0, 0, Sell01 + Sell11 + Sell02 + Sell12 - Volume), If(Volume < Sell01 + Sell02 + Sell03 + Sell11 + Sell12 + Sell13, If(Sell03 == 0, 0, Sell01 + Sell02 + Sell03 + Sell11 + Sell12 + Sell13 - Volume), 0), If(And(Operation == StringVal("Sell"), Price == 101), If(Volume > Buy11 + Buy12 + Buy13, 0, Sell01), If(Sell01 == 0, If(Volume > Buy01 + Buy02 + Buy03, Volume - Buy01 - Buy02 - Buy03, 0), Sell01)))))))))

def NextSell02(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), If(Sell01 != 0, Sell02, If(Sell01 != 0, Sell02, If(Sell02 != 0, If(Volume < Sell11, Sell02, Sell03), 0), If(And(Operation == StringVal("Buy"), Price == 102), If(Volume < Sell01 + Sell11, Sell02, If(Volume < Sell01 + Sell11 + Sell02 + Sell12, Sell03, 0), If(And(Operation == StringVal("Sell"), Price == 101), If(Sell11 == 0, If(Volume > Buy01 + Buy02 + Buy03 + Buy11 + Buy12 + Buy13, Sell01, Sell02), Sell01), If(And(Sell01 == 0, Sell11 == 0), 0, If(And(Sell02 == 0, Sell12 == 0), Volume, Sell02))))))))

def NextSell03(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), If(Sell11 == 0, Sell03, If(Volume >= Sell11, 0, Sell03), If(And(Operation == StringVal("Buy"), Price == 102), If(Volume < Sell01 + Sell11, Sell03, 0), If(And(Operation == StringVal("Sell"), Price == 101), If(Volume > Buy01 + Buy02 + Buy03 + Buy11 + Buy12 + Buy13, Sell02, Sell03), If(Sell02 + Sell12 != 0, Volume, 0)))))

def NextBuy13(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), If(Or(Buy12 != 0, Buy02 != 0), Volume, 0), If(And(Operation == StringVal("Buy"), Price == 102), If(Volume < Sell01 + Sell02 + Sell03 + Sell11 + Sell12 + Sell13, Buy13, Buy12), If(And(Operation == StringVal("Sell"), Price == 101), If(Volume < Buy01 + Buy11, Buy13, 0), If(Buy01 == 0, Buy13, If(Volume < Buy01, Buy13, 0)))))

def NextBuy12(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), If(Buy02 + Buy12 != 0, Buy12, If(Buy01 + Buy11 != 0, Volume, 0), If(And(Operation == StringVal("Buy"), Price == 102), Buy11, If(And(Operation == StringVal("Sell"), Price == 101), If(Volume < Buy01 + Buy11, Buy12, If(Volume < Buy01 + Buy11 + Buy02 + Buy12, Buy13, 0), If(Buy01 == 0, Buy12, If(Buy02 == 0, If(Volume < Buy01, Buy12, Buy13), If(Buy03 == 0, If(Volume < Buy01, Buy12, If(Volume < Buy01 + Buy02, Buy13, 0), If(Volume < Buy01, Buy12, If(Volume < Buy01 + Buy02, Buy13, 0)))))))))))

def NextBuy11(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), If(Buy01 != 0, 0, If(And(Sell01 + Sell11 == 0, Buy01 + Buy11 != 0), Buy11, If(Sell11 == 0, Volume, If(Sell01 != 0, Buy11, If(Buy12 != 0, Buy12, If(Sell02 != 0, If(Volume < Sell11, 0, Volume - Sell11), If(Sell03 != 0, If(Volume < Sell11 + Sell12, 0, Volume - Sell11 - Sell12), If(Volume < Sell11 + Sell12 + Sell13, 0, Volume - Sell11 - Sell12 - Sell13), If(And(Operation == StringVal("Buy"), Price == 102), 0, If(And(Operation == StringVal("Sell"), Price == 101), If(Volume < Buy01 + Buy11, If(Buy11 == 0, 0, Buy11 - Volume), If(Volume < Buy01 + Buy11 + Buy02 + Buy12, If(Buy12 == 0, 0, Buy12 + Buy11 + Buy01 - Volume), If(Or(Buy13 == 0, Buy13 + Buy11 + Buy01 + Buy02 + Buy12 - Volume < 0), 0, Buy13 + Buy11 + Buy01 + Buy02 + Buy12 - Volume), If(Buy01 == 0, Buy11, If(Buy02 == 0, If(Volume < Buy01, 0, Buy12), If(Buy03 == 0, If(Volume < Buy01, 0, If(Volume < Buy01 + Buy02, 0, Buy13), 0))))))))))))))))

def NextSell11(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), If(Sell01 != 0, 0, If(Sell11 == 0, 0, If(Volume < Sell11, Sell11 - Volume, If(Volume < Sell11 + Sell12, If(Sell12 == 0, 0, Sell11 + Sell12 - Volume), If(Volume < Sell11 + Sell12 + Sell13, If(Sell13 == 0, 0, Sell11 + Sell12 + Sell13 - Volume), 0), If(And(Operation == StringVal("Buy"), Price == 102), If(Sell11 == 0, 0, If(Sell12 == 0, If(Volume >= Sell11, 0, Sell11 - Volume), If(Sell13 == 0, If(Volume < Sell11, Sell11 - Volume, If(Volume < Sell11 + Sell12, Sell11 + Sell12 - Volume, If(Volume < Sell11, Sell11 - Volume, If(Volume < Sell11 + Sell12, Sell11 + Sell12 - Volume, If(Volume < Sell11 + Sell12 + Sell13, Sell11 + Sell12 + Sell13 - Volume, 0), If(Volume < Sell11, Sell11 - Volume, 0), If(And(Operation == StringVal("Sell"), Price == 101), If(Sell11 != 0, Sell11, If(Volume <= Buy01 + Buy11 + Buy02 + Buy12 + Buy03 + Buy13, 0, Volume - Buy01 - Buy11 - Buy02 - Buy12 - Buy03 - Buy13), Sell11)))))))))))))))

def NextSell12(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), If(Sell01 != 0, 0, If(Volume < Sell11, Sell12, If(Volume < Sell11 + Sell12, Sell13, 0), If(And(Operation == StringVal("Buy"), Price == 102), If(Volume < Sell01 + Sell11, Sell12, If(Volume < Sell01 + Sell11 + Sell02 + Sell12, Sell13, 0), If(And(Operation == StringVal("Sell"), Price == 101), If(Sell11 == 0, 0, If(Sell12 != 0, Sell12, Volume), Sell12)))))))

def NextSell13(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(And(Operation == StringVal("Buy"), Price == 101), If(And(Sell13 != 0, Volume >= Sell11), 0, Sell13), If(And(Operation == StringVal("Buy"), Price == 102), If(Volume >= Sell01 + Sell11, 0, Sell13), If(And(Operation == StringVal("Sell"), Price == 101), If(Sell12 != 0, Volume, 0), 0)))

def IsPossible(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
	return If(Or(And(Buy02 + Buy12 != 0, Operation == StringVal("Buy"), Price == 101), And(Sell03 != 0, Operation == StringVal("Sell"), Price == 102)), False, True)

def Symb(x):
	return If(x < 2, str(x), StringVal("M"))

def GetHyperState(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13):
	return Symb(Buy03) + Symb(Buy02) + Symb(Buy01) + Symb(Sell01) + Symb(Sell02) + Symb(Sell03) + StringVal("-") + Symb(Buy13) + Symb(Buy12) + Symb(Buy11) + Symb(Sell11) + Symb(Sell12) + Symb(Sell13)

def GetInfo():
	return [12, 3, [StringVal("Buy"), StringVal("Sell")], [101, 102], [1, 2, 3, 4, 5, 6, 7, 8, 9]]

def GetStartPosition():
	return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def StopCondition(a, b, c, d, e, f, g, h, i, j, k, l):
	return False
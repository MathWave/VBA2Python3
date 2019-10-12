from z3 import *



def NextBid2(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
	return If(And(((Order_Type == StringVal("Buy")), (Bid_1 > 0), (Bid_2 == 0))), Order_Volume, If(And(((Order_Type == StringVal("Sell")), (Order_Volume >= Bid_1))), 0, Bid_2))

def NextBid1(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
	return If(And((Order_Type == StringVal("Buy")), (Bid_1 == 0), (Order_Volume >= Ask_1 + Ask_2)), Order_Volume - Ask_1 - Ask_2, If(And(((Order_Type == StringVal("Sell")), (Bid_1 > 0), (Order_Volume < Bid_1))), Bid_1 - Order_Volume, If(And(((Order_Type == StringVal("Sell")), (Bid_1 > 0), (Order_Volume < Bid_1 + Bid_2))), Bid_1 + Bid_2 - Order_Volume, If(And(((Order_Type == StringVal("Sell")), (Bid_1 > 0), (Order_Volume >= Bid_1 + Bid_2))), 0, Bid_1))))

def NextAsk1(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
	return If(And((Order_Type == StringVal("Sell")), (Ask_1 == 0), (Order_Volume >= Bid_1 + Bid_2)), Order_Volume - Bid_1 - Bid_2, If(And((Order_Type == StringVal("Buy")), (Ask_1 > 0), (Order_Volume < Ask_1)), Ask_1 - Order_Volume, If(And(((Order_Type == StringVal("Buy")), (Ask_1 > 0), (Order_Volume < Ask_1 + Ask_2))), Ask_1 + Ask_2 - Order_Volume, If(And(((Order_Type == StringVal("Buy")), (Ask_1 > 0), (Order_Volume >= Ask_1 + Ask_2))), 0, Ask_1))))

def NextAsk2(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
	return If(And(((Order_Type == StringVal("Sell")), (Ask_1 > 0), (Ask_2 == 0))), Order_Volume, If(And(((Order_Type == StringVal("Buy")), (Order_Volume >= Ask_1))), 0, Ask_2))

def HSymb(x):
	return If(x == 1, StringVal("1"), If(x == 0, StringVal("0"), StringVal("M")))

def GetHyperState(X1, X2, X3, X4):
	return HSymb(X1) + HSymb(X2) + StringVal("|") + HSymb(X3) + HSymb(X4)

def IsPossible(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
	return If(Or(And(Bid_2 != 0, Order_Type == StringVal("Buy")), And(Ask_2 != 0, Order_Type == StringVal("Sell"))), False, True)

def GetStartPosition():
	return [0, 0, 0, 0]

def StopCondition(first, second, third, forth):
	return False

def GetInfo():
	return [4, 3, [StringVal("Buy"), StringVal("Sell")], [101], [1, 2, 3, 4, 5, 6, 7, 8, 9]]

def NextCurrent(current, data):
	return [NextBid2(*current, *data), NextBid1(*current, *data), NextAsk1(*current, *data), NextAsk2(*current, *data)]


arr = []
for i in range(11):
	arr.append(Int('x_' + str(i)))
arr[8] = String('x_8')
	
solve(GetHyperState(arr[0], arr[1], arr[2], arr[3]) == StringVal('00|00'),
	  GetHyperState(arr[4], arr[5], arr[6], arr[7]) == StringVal('00|M0'),
	  NextCurrent([arr[0], arr[1], arr[2], arr[3]], [arr[8], arr[9], arr[10]])[0] == [arr[4], arr[5], arr[6], arr[7]][0],
	  NextCurrent([arr[0], arr[1], arr[2], arr[3]], [arr[8], arr[9], arr[10]])[1] == [arr[4], arr[5], arr[6], arr[7]][1],
	  NextCurrent([arr[0], arr[1], arr[2], arr[3]], [arr[8], arr[9], arr[10]])[2] == [arr[4], arr[5], arr[6], arr[7]][2],
	  NextCurrent([arr[0], arr[1], arr[2], arr[3]], [arr[8], arr[9], arr[10]])[3] == [arr[4], arr[5], arr[6], arr[7]][3],
	  )
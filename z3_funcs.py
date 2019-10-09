from z3 import *

def NextBid2(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
	return If(((Order_Type == "Buy") and (Bid_1 > 0) and (Bid_2 == 0)), Order_Volume, If(((Order_Type == "Sell") and (Order_Volume >= Bid_1)), 0, Bid_2)def NextBid1(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
def NextAsk1(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
def NextAsk2(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
def HSymb(x):
def GetHyperState(X1, X2, X3, X4):
def IsPossible(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
def GetStartPosition():
def StopCondition(first, second, third, forth):
def GetInfo():

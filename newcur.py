from transpep import *

def NextCurrent(current, data):
	return [NextBid2(*current, *data), NextBid1(*current, *data), NextAsk1(*current, *data), NextAsk2(*current, *data)]
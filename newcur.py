from transpep import *

def NextCurrent(current, data):
	return [NextBuy03(*current, *data), NextBuy02(*current, *data), NextBuy01(*current, *data), NextSell01(*current, *data), NextSell02(*current, *data), NextSell03(*current, *data), NextBuy13(*current, *data), NextBuy12(*current, *data), NextBuy11(*current, *data), NextSell11(*current, *data), NextSell12(*current, *data), NextSell13(*current, *data)]
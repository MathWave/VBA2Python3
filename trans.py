def NextBid2(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):

    if ((Order_Type == "Buy") and (Bid_1 > 0) and (Bid_2 == 0)):
        return Order_Volume
    else:
        if ((Order_Type == "Sell") and (Order_Volume >= Bid_1)):
            return 0
        else:
            return Bid_2
        
    



def NextBid1(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
  
    if (Order_Type == "Buy") and (Bid_1 == 0) and (Order_Volume >= Ask_1 + Ask_2):
        return Order_Volume - Ask_1 - Ask_2
    elif ((Order_Type == "Sell") and (Bid_1 > 0) and (Order_Volume < Bid_1)):
        return Bid_1 - Order_Volume
    elif ((Order_Type == "Sell") and (Bid_1 > 0) and (Order_Volume < Bid_1 + Bid_2)):
        return Bid_1 + Bid_2 - Order_Volume
    elif ((Order_Type == "Sell") and (Bid_1 > 0) and (Order_Volume >= Bid_1 + Bid_2)):
        return 0
    else:
        return Bid_1
    



def NextAsk1(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
    
    if (Order_Type == "Sell") and (Ask_1 == 0) and (Order_Volume >= Bid_1 + Bid_2):
        return Order_Volume - Bid_1 - Bid_2
    else:
        if (Order_Type == "Buy") and (Ask_1 > 0) and (Order_Volume < Ask_1):
            return Ask_1 - Order_Volume
        else:
            if ((Order_Type == "Buy") and (Ask_1 > 0) and (Order_Volume < Ask_1 + Ask_2)):
                return Ask_1 + Ask_2 - Order_Volume
            else:
                if ((Order_Type == "Buy") and (Ask_1 > 0) and (Order_Volume >= Ask_1 + Ask_2)):
                    return 0
                else:
                    return Ask_1
                
            
        
    



def NextAsk2(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):

    if ((Order_Type == "Sell") and (Ask_1 > 0) and (Ask_2 == 0)):
        return Order_Volume
    else:
        if ((Order_Type == "Buy") and (Order_Volume >= Ask_1)):
            return 0
        else:
            return Ask_2
        
    




def HSymb(x):

    if x <= 1:
        return str(x)
    else:
        return "M"

    
    



def GetHyperState(X1, X2, X3, X4):

    return HSymb(X1) + HSymb(X2) + "|" + HSymb(X3) + HSymb(X4)
    



def IsPossible(Bid_2, Bid_1, Ask_1, Ask_2, Order_Type, Order_Price, Order_Volume):
    if Bid_2 != 0 and Order_Type == "Buy" or Ask_2 != 0 and Order_Type == "Sell":
        return False
    else:
        return True


def GetStartPosition():
    return [0,0,0,0]


def StopCondition(first, second, third, forth):
    return False


def GetInfo():
    return [4, 3, ["Buy", "Sell"], [101], [1, 2, 3, 4, 5, 6, 7, 8, 9]]

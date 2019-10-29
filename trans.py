def NextBuy03(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            return Buy03
    elif Operation == "Buy" and Price == 102:
            if Buy02 != 0:
                return Volume
            else:
                return Buy03
            
    elif Operation == "Sell" and Price == 101:
            if Volume >= Buy01 + Buy11:
                return 0
            else:
                return Buy03
            
    else:
            if Buy01 == 0:
                return Buy03
            elif Volume >= Buy01:
                return 0
            else:
                return Buy03
            
    


def NextBuy02(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            return Buy02
    elif Operation == "Buy" and Price == 102:
            if Buy01 == 0:
                return 0
            elif Buy02 != 0:
                return Buy02
            else:
                return Volume
            
    elif Operation == "Sell" and Price == 101:
            if Volume < Buy01 + Buy11:
                return Buy02
            elif Volume < Buy01 + Buy02 + Buy11 + Buy12:
                return Buy03
            else:
                return 0
            
    else:
            if Buy02 == 0:
                return 0
            else:
                if Volume < Buy01:
                    return Buy02
                elif Volume < Buy01 + Buy02:
                    return Buy03
                else:
                    return 0
                
            
    


def NextBuy01(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            return Buy01
    elif Operation == "Buy" and Price == 102:
            if Buy01 == 0:
                if Sell01 + Sell11 == 0:
                    return Volume
                elif Sell02 + Sell12 == 0:
                    if Volume > Sell01 + Sell11:
                        return Volume - Sell01 - Sell11
                    else:
                        return 0
                    
                elif Sell03 + Sell13 == 0:
                    if Volume > Sell01 + Sell11 + Sell02 + Sell12:
                        return Volume - Sell01 - Sell11 - Sell02 - Sell12
                    else:
                        return 0
                    
                else:
                    if Volume > Sell01 + Sell02 + Sell03 + Sell11 + Sell12 + Sell13:
                        return Volume - Sell01 - Sell02 - Sell03 - Sell11 - Sell12 - Sell13
                    else:
                        return 0
                    
                
            else:
                return Buy01
            
    elif Operation == "Sell" and Price == 101:
            if Buy01 == 0:
                return 0
            elif Buy02 == 0:
                if Volume >= Buy01:
                    return 0
                else:
                    return Buy01 - Volume
                
            elif Buy03 == 0:
                if Volume < Buy01:
                    return Buy01 - Volume
                elif Volume < Buy01 + Buy02:
                    return Buy01 + Buy02 - Volume
                else:
                    return 0
                
            else:
                if Volume < Buy01:
                    return Buy01 - Volume
                elif Volume < Buy01 + Buy02:
                    return Buy01 + Buy02 - Volume
                elif Volume < Buy01 + Buy02 + Buy03:
                    return Buy01 + Buy02 + Buy03 - Volume
                else:
                    return 0
                
            
    else:
            if Buy01 == 0:
                return 0
            elif Buy02 == 0:
                if Volume >= Buy01:
                    return 0
                else:
                    return Buy01 - Volume
                
            elif Buy03 == 0:
                if Volume < Buy01:
                    return Buy01 - Volume
                elif Volume < Buy01 + Buy02:
                    return Buy01 + Buy02 - Volume
                else:
                    return 0
                
            else:
                if Volume < Buy01:
                    return Buy01 - Volume
                elif Volume < Buy01 + Buy02:
                    return Buy01 + Buy02 - Volume
                elif Volume < Buy01 + Buy02 + Buy03:
                    return Buy01 + Buy02 + Buy03 - Volume
                else:
                    return 0
                
            

    


def NextSell01(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            if Sell01 != 0:
                return Sell01
            elif Sell02 != 0:
                if Volume < Sell11:
                    return Sell01
                else:
                    return Sell02
                
            elif Sell03 != 0:
                if Volume < Sell11:
                    return Sell01
                elif Volume < Sell11 + Sell12:
                    return Sell02
                else:
                    return Sell03
                
            else:
                return 0
            
    elif Operation == "Buy" and Price == 102:
            if Volume < Sell01 + Sell11:
                if Sell01 == 0:
                    return 0
                else:
                    return Sell01 + Sell11 - Volume
                
            elif Volume < Sell01 + Sell11 + Sell02 + Sell12:
                if Sell02 == 0:
                    return 0
                else:
                    return Sell01 + Sell11 + Sell02 + Sell12 - Volume
                
            elif Volume < Sell01 + Sell02 + Sell03 + Sell11 + Sell12 + Sell13:
                if Sell03 == 0:
                    return 0
                else:
                    return Sell01 + Sell02 + Sell03 + Sell11 + Sell12 + Sell13 - Volume
                
            else:
                return 0
            
    elif Operation == "Sell" and Price == 101:
            if Volume > Buy11 + Buy12 + Buy13:
                return 0
            else:
                return Sell01
            
    else:
            if Sell01 == 0:
                if Volume > Buy01 + Buy02 + Buy03:
                    return Volume - Buy01 - Buy02 - Buy03
                else:
                    return 0
                
            else:
                return Sell01
            
    


def NextSell02(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            if Sell01 != 0:
                return Sell02
            else:
                if Sell01 != 0:
                    return Sell02
                elif Sell02 != 0:
                    if Volume < Sell11:
                        return Sell02
                    else:
                        return Sell03
                    
                else:
                    return 0
                
            
    elif Operation == "Buy" and Price == 102:
            if Volume < Sell01 + Sell11:
                return Sell02
            elif Volume < Sell01 + Sell11 + Sell02 + Sell12:
                return Sell03
            else:
                return 0
            
    elif Operation == "Sell" and Price == 101:
            if Sell11 == 0:
                if Volume > Buy01 + Buy02 + Buy03 + Buy11 + Buy12 + Buy13:
                    return Sell01
                else:
                    return Sell02
                
            else:
                return Sell01
            
    else:
            if Sell01 == 0 and Sell11 == 0:
                return 0
            elif Sell02 == 0 and Sell12 == 0:
                return Volume
            else:
                return Sell02
            
    


def NextSell03(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            if Sell11 == 0:
                return Sell03
            else:
                if Volume >= Sell11:
                    return 0
                else:
                    return Sell03
                
            
    elif Operation == "Buy" and Price == 102:
            if Volume < Sell01 + Sell11:
                return Sell03
            else:
                return 0
            
    elif Operation == "Sell" and Price == 101:
            if Volume > Buy01 + Buy02 + Buy03 + Buy11 + Buy12 + Buy13:
                return Sell02
            else:
                return Sell03
            
    else:
            if Sell02 + Sell12 != 0:
                return Volume
            else:
                return 0
            
    


def NextBuy13(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            if Buy12 != 0 or Buy02 != 0:
                return Volume
            else:
                return 0
            
    elif Operation == "Buy" and Price == 102:
            if Volume < Sell01 + Sell02 + Sell03 + Sell11 + Sell12 + Sell13:
                return Buy13
            else:
                return Buy12
            
    elif Operation == "Sell" and Price == 101:
            if Volume < Buy01 + Buy11:
                return Buy13
            else:
                return 0
            
    else:
            if Buy01 == 0:
                return Buy13
            else:
                if Volume < Buy01:
                    return Buy13
                else:
                    return 0
                
            
    


def NextBuy12(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            if Buy02 + Buy12 != 0:
                return Buy12
            elif Buy01 + Buy11 != 0:
                return Volume
            else:
                return 0
            
    elif Operation == "Buy" and Price == 102:
            return Buy11
    elif Operation == "Sell" and Price == 101:
            if Volume < Buy01 + Buy11:
                return Buy12
            elif Volume < Buy01 + Buy11 + Buy02 + Buy12:
                return Buy13
            else:
                return 0
            
    else:
            if Buy01 == 0:
                return Buy12
            elif Buy02 == 0:
                if Volume < Buy01:
                    return Buy12
                else:
                    return Buy13
                
            elif Buy03 == 0:
                if Volume < Buy01:
                    return Buy12
                elif Volume < Buy01 + Buy02:
                    return Buy13
                else:
                    return 0
                
            else:
                if Volume < Buy01:
                    return Buy12
                elif Volume < Buy01 + Buy02:
                    return Buy13
                else:
                    return 0
                
            
    


def NextBuy11(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            if Buy01 != 0:
                return 0
            elif Sell01 + Sell11 == 0 and Buy01 + Buy11 != 0:
                return Buy11
            elif Sell11 == 0:
                return Volume
            else:
                if Sell01 != 0:
                    return Buy11
                elif Buy12 != 0:
                    return Buy12
                elif Sell02 != 0:
                    if Volume < Sell11:
                        return 0
                    else:
                        return Volume - Sell11
                    
                elif Sell03 != 0:
                    if Volume < Sell11 + Sell12:
                        return 0
                    else:
                        return Volume - Sell11 - Sell12
                    
                else:
                    if Volume < Sell11 + Sell12 + Sell13:
                        return 0
                    else:
                        return Volume - Sell11 - Sell12 - Sell13
                    
                
            
    elif Operation == "Buy" and Price == 102:
            return 0
    elif Operation == "Sell" and Price == 101:
            if Volume < Buy01 + Buy11:
                if Buy11 == 0:
                    return 0
                else:
                    return Buy11 - Volume
                
            elif Volume < Buy01 + Buy11 + Buy02 + Buy12:
                if Buy12 == 0:
                    return 0
                else:
                    return Buy12 + Buy11 + Buy01 - Volume
                
            else:
                if Buy13 == 0 or Buy13 + Buy11 + Buy01 + Buy02 + Buy12 - Volume < 0:
                    return 0
                else:
                    return Buy13 + Buy11 + Buy01 + Buy02 + Buy12 - Volume
                
            
    else:
            if Buy01 == 0:
                return Buy11
            elif Buy02 == 0:
                if Volume < Buy01:
                    return 0
                else:
                    return Buy12
                
            elif Buy03 == 0:
                if Volume < Buy01:
                    return 0
                elif Volume < Buy01 + Buy02:
                    return 0
                else:
                    return Buy13
                
            else:
                return 0
            
    


def NextSell11(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            if Sell01 != 0:
                return 0
            elif Sell11 == 0:
                return 0
            else:
                if Volume < Sell11:
                    return Sell11 - Volume
                elif Volume < Sell11 + Sell12:
                    if Sell12 == 0:
                        return 0
                    else:
                        return Sell11 + Sell12 - Volume
                    
                elif Volume < Sell11 + Sell12 + Sell13:
                    if Sell13 == 0:
                        return 0
                    else:
                        return Sell11 + Sell12 + Sell13 - Volume
                    
                else:
                    return 0
                
            
    elif Operation == "Buy" and Price == 102:
            if Sell11 == 0:
                return 0
            elif Sell12 == 0:
                if Volume >= Sell11:
                    return 0
                else:
                    return Sell11 - Volume
                
            elif Sell13 == 0:
                if Volume < Sell11:
                    return Sell11 - Volume
                elif Volume < Sell11 + Sell12:
                    return Sell11 + Sell12 - Volume
                else:
                    if Volume < Sell11:
                        return Sell11 - Volume
                    elif Volume < Sell11 + Sell12:
                        return Sell11 + Sell12 - Volume
                    elif Volume < Sell11 + Sell12 + Sell13:
                        return Sell11 + Sell12 + Sell13 - Volume
                    else:
                        return 0
                    
                
            else:
                if Volume < Sell11:
                    return Sell11 - Volume
                else:
                    return 0
                
            
    elif Operation == "Sell" and Price == 101:
            if Sell11 != 0:
                return Sell11
            else:
                if Volume <= Buy01 + Buy11 + Buy02 + Buy12 + Buy03 + Buy13:
                    return 0
                else:
                    return Volume - Buy01 - Buy11 - Buy02 - Buy12 - Buy03 - Buy13
                
            
    else:
            return Sell11
    


def NextSell12(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            if Sell01 != 0:
                return 0
            else:
                if Volume < Sell11:
                    return Sell12
                elif Volume < Sell11 + Sell12:
                    return Sell13
                else:
                    return 0
                
            
    elif Operation == "Buy" and Price == 102:
            if Volume < Sell01 + Sell11:
                return Sell12
            elif Volume < Sell01 + Sell11 + Sell02 + Sell12:
                return Sell13
            else:
                return 0
            
    elif Operation == "Sell" and Price == 101:
            if Sell11 == 0:
                return 0
            elif Sell12 != 0:
                return Sell12
            else:
                return Volume
            
    else:
            return Sell12
    


def NextSell13(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Operation == "Buy" and Price == 101:
            if Sell13 != 0 and Volume >= Sell11:
                return 0
            else:
                return Sell13
            
    elif Operation == "Buy" and Price == 102:
            if Volume >= Sell01 + Sell11:
                return 0
            else:
                return Sell13
            
    elif Operation == "Sell" and Price == 101:
            if Sell12 != 0:
                return Volume
            else:
                return 0
            
    else:
            return 0
    


def IsPossible(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13, Operation, Price, Volume):
    if Buy02 + Buy12 != 0 and Operation == "Buy" and Price == 101 or Sell03 != 0 and Operation == "Sell" and Price == 102:
        return False
    else:
        if Buy03 < 0 or Buy02 < 0 or Buy01 < 0 or Sell01 < 0 or Sell02 < 0 or Sell03 < 0 or Buy13 < 0 or Buy12 < 0 or Buy11 < 0 or Sell11 < 0 or Sell12 < 0 or Sell13 < 0:
            return False
        else:
            if Operation == "Buy" or Operation == "Sell":
                if Price == 101 or Price == 102:
                    return True
                else:
                    return False
                
            else:
                return False
            
        
    


def Symb(x):
    if x == 0:
        return "0"
    else:
        return "M"


def GetHyperState(Buy03, Buy02, Buy01, Sell01, Sell02, Sell03, Buy13, Buy12, Buy11, Sell11, Sell12, Sell13):
    return Symb(Buy03) + Symb(Buy02) + Symb(Buy01) + Symb(Sell01) + Symb(Sell02) + Symb(Sell03) + "-" + Symb(Buy13) + Symb(Buy12) + Symb(Buy11) + Symb(Sell11) + Symb(Sell12) + Symb(Sell13)


def GetInfo():
    return [12, 3, ["Buy", "Sell"], [101, 102], [1, 2, 3, 4, 5, 6, 7, 8, 9]]


def GetStartPosition():
    return [0,0,0,0,0,0,0,0,0,0,0,0]


def StopCondition(a,b,c,d,e,f,g,h,i,j,k,l):
    return False



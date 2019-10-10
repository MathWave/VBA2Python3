def Next(a, b):
    if a < b:
        return 1
    else:
        return 0

def Add(a, b, c):
    if a < b:
        return 2
    else:
        if b < c:
            return 1
        else:
            return 0

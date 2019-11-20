a = 0
try:
    a = 1/0
except Exception as e:
    print(str(e))
import sys
ENC = [60, 54, 59, 61, 33, 107, 52, 44, 105, 40, 46, 5, 46, 50, 105, 5, 57, 50, 105, 57, 49, 5, 54, 106, 61, 107, 57, 39]
KEY = 0x5A
s = sys.argv[1] if len(sys.argv) > 1 else input('pass: ')
if len(s) == len(ENC) and all((ord(c) ^ KEY) == e for c, e in zip(s, ENC)):
    print('ACCESS GRANTED:', s)
else:
    print('DENIED')

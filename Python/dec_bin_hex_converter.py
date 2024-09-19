#Decimal_Binary_Hexadecimal_Rechner
type = int(input("Decimal = 1"+" Binary = 2"+" Hex = 3"+" : "))
excalcobj = input("your number : ")
def dec2bin(excalcobj):
    number = bin(int(excalcobj))
    bincalcobj = number
    return bincalcobj
def dec2hex(excalcobj):
    number = hex(int(excalcobj))
    hexcalcobj = number
    return hexcalcobj
def bin2dec(excalcobj):
    number = int(excalcobj,2)
    deccalcobj = number
    return deccalcobj
def bin2hex(excalcobj):
    number = hex(int(excalcobj,2))
    hexcalcobj = number
    return hexcalcobj
def hex2dec(excalcobj):
    number = int(excalcobj,16)
    deccalcobj = number
    return deccalcobj
def hex2bin(excalcobj):
    number = bin(int(excalcobj,16))
    bincalcobj = number
    return bincalcobj
def calc(type,excalcobj):
    if type == 1:
     
     dec = excalcobj
     bin = dec2bin(excalcobj)
     hex = dec2hex(excalcobj)
     print(dec,bin,hex)
     return 
    if type == 2:
     
     dec = bin2dec(excalcobj)
     bin = excalcobj
     hex = bin2hex(excalcobj)
     print(dec,bin,hex)
     return  
    if type == 3:
     
     dec = hex2dec(excalcobj)
     bin = hex2bin(excalcobj)
     hex = excalcobj
     print(dec,bin,hex)
     return
    else :
     dec = "unbekannt"
     bin = "unbekannt"
     hex = "unbekannt"
     print(dec,bin,hex)
     return 
calc(type,excalcobj)

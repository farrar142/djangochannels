#SYSTEM CODE#
SUCCEED = "SUCCEED"
FAILED = "FAILED"
NONE = "NONE"

#TYPE
BUY = 1
SELL = 2

#CODE
NORMAL = 1
COMPLETE = 2
CANCELED = 3
HOLD = 4
MARKET = 5

#EVENT
SIGNUP = 1
EVENT1 = 2

#BOOLEANWRAPPER
true = True
false = False




        
def fail_message(msg:str):
    return {'system':{
        "result": FAILED,
        "messages":msg
    }}
        
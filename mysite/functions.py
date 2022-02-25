
from time import time as dt
from pprint import pprint
def timer(cb):
    def wrap(*args,**kwargs):
        
        start = dt()
        
        result = cb(*args,**kwargs)
        
        end = dt()
        print(f"{cb.__name__} : ellapsed {end-start:0.5f}sec")
        pprint(kwargs)
        return result
    
    return wrap

def checker(cb):
    def wrap(*args,**kwargs):
        print(f"{cb.__name__} started")
        result = cb
        print(f"{cb.__name__} finished")
        return result
    return wrap

def value_parser(target):
    
    result = str(target).lstrip('[').rstrip(']')
    return result
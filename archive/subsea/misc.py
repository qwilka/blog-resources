##import logging
from math import pi

from miscfunclib import is_number

##logger = logging.getLogger(__name__)



def pipe_coating(D, *aargs):
    _ERROR = False
    if len(aargs) % 2 == 1:
        _ERROR = True
    if not _ERROR:
        for ii in aargs:
            if is_number(ii) and ii>0:
                continue
            else:
                _ERROR = True 
    if _ERROR:
        ##logger.error("Error in function pipe_coating: thickness, density arguments not spectified correctly")
        raise ValueError("Error in function pipe_coating: thickness, density arguments not spectified correctly")
    #thk_den = list(zip(ll[::2], ll[1::2]))
        
    Dcoat = D
    WTcoat = 0
    mass_coat = 0
    
    for thk, den in list(zip(aargs[::2], aargs[1::2])):
        Dcoat_o = Dcoat + thk
        Acoat = pi/4 * (Dcoat_o**2 - Dcoat**2)
        WTcoat = 0
    

if __name__=="__main__":
    pipe_coating(0.3, 1,2)
    pipe_coating(0.3, 1,2,3)
        
import os

class RateLimiter:
    __isfileopen :bool = False
    __sameplefile=os.path.basename(__file__)
    def __init__(self,ip_adrs,filename=__sameplefile):
        self.ip=ip_adrs
        print(filename)
        pass
    def __Fileopener(self,Filename):
            pass
    
    
if __name__=="__main__":
    t=RateLimiter(12)
    print(t)
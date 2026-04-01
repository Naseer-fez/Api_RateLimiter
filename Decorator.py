from ARL import Ratelimiter
from flask import request
from pathlib import Path
import sys

__Filename=Path(sys.modules['__main__'].__file__).stem

def RequiredRateLimiter(Cleaning=False,
                CooldownTime=20,AllowedFreq=8,CleaningFreq=80,ResetTime=8,Filename=__Filename,FolderPath=None,FileType=".json"):
        def Decorator(Func):
            def Wrapper(*args,**kwargs):
                Ip=request.remote_addr
                CoolDown=Ratelimiter(IP_Adrs=Ip,*args,**kwargs)

                if CoolDown==1:
                    return Func(*args, **kwargs)
                else:
                    return f"Rate limit exceeded. Please wait {CoolDown} Secs.", 429    
            return Wrapper
        return Decorator
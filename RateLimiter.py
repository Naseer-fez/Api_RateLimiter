from pathlib import Path
import sys
__isfileopen :bool = False
___samplefile = Path(sys.modules['__main__'].__file__).stem
def ARL(IP_Adrs:str,Cleaning=False,AutoUpdate=False,
                CooldownTime=20,AllowedFreq=8,CleaningFreq=80,ResetTime=8,UpdateFreq=8,Filename=___samplefile,FolderPath=None,Format="sql")->int:
    if Format.lower()=="json":
        from  ARL import Ratelimiter as Rl
        return Rl(
            IP_Adrs=IP_Adrs,Cleaning=Cleaning,AutoUpdate=AutoUpdate,
                CooldownTime=CooldownTime,AllowedFreq=AllowedFreq,CleaningFreq=CleaningFreq,ResetTime=ResetTime,
                UpdateFreq=UpdateFreq,Filename=Filename,FolderPath=FolderPath)        
    elif Format.lower()=="sql" :
        from ARL_sql import Ratelimiter as Rl
        return Rl(
                IP_Adrs=IP_Adrs,Cleaning=Cleaning,AutoUpdate=AutoUpdate,
                    CooldownTime=CooldownTime,AllowedFreq=AllowedFreq,CleaningFreq=CleaningFreq,ResetTime=ResetTime,
                    UpdateFreq=UpdateFreq,Filename=Filename,FolderPath=FolderPath)
    else:
        from ARL_Nostorage import Ratelimiter as Rl
        return Rl(IP_Adrs=IP_Adrs,Cleaning=Cleaning,CleaningFreq=CleaningFreq,AllowedFreq=AllowedFreq,ResetTime=ResetTime)
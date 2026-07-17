from pathlib import Path
import sys
__isfileopen :bool = False
_main_file = getattr(sys.modules.get('__main__'), '__file__', None)
___samplefile = Path(_main_file).stem if _main_file else "sample"
def ARL(IP_Adrs:str,Cleaning=False,AutoUpdate=False,
                CooldownTime=20,AllowedFreq=8,CleaningFreq=80,ResetTime=8,UpdateFreq=8,Filename=___samplefile,FolderPath=None,Format=None)->int:
    if Format is None:
        from ARL_nostorage import Ratelimiter as Rl
        return Rl(IP_Adrs=IP_Adrs,Cleaning=Cleaning,CleaningFreq=CleaningFreq,
                  CooldownTime=CooldownTime,AllowedFreq=AllowedFreq,ResetTime=ResetTime)
    elif (isinstance(Format,str) is False):
        raise TypeError("Only String Option is Availabe for Format Option")
    elif (Format.lower())=="json":
        from  ARL_json import Ratelimiter as Rl
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
    else :
        raise TypeError("""
        Format Extensions available here  
        is not valid please provide a valid extension,
        Availabe : Sql,json,Nostorage
        Format : json,sql ,(Python (None))
        """)
import os
import sys
from pathlib import Path
import json
import time
import ipaddress
import threading
class RateLimiter:
    __isfileopen :bool = False
    __samplefile = Path(sys.modules['__main__'].__file__).stem
    def __init__(self,ip_adrs,filename=__samplefile,filetype="json",folder=None):
        self.thread_running = False
        self.filename=filename 
        self.filetype=filetype
        self.Data=dict()
        self.CurrentFile=None
        self.fullpath=os.path.join(folder or "", f"{filename}.{filetype}")
        self.Validopen=self.__Fileopener()
        self.API_RL(IP_Adrs=ip_adrs)
        pass
    def API_RL(self,IP_Adrs:str,Cleaning=False,
               CooldownTime=20,AllowedFreq=8,MinAttempts=10,CleaningFreq=False
               ):
        # if isinstance(ipaddress,str):
        #     self.ip=int(ipaddress.ip_address(IP_Adrs))
        # else:
        #     self.ip=IP_Adrs
        self.Metrics={
            "Cooldowntime":CooldownTime,
            "AllowedFreq":AllowedFreq,
            "MinAttempts":MinAttempts }
        # background_thread = threading.Thread(target=self.hehe, args=(start_val,), daemon=True)
        if (not self.thread_running) and (Cleaning or CleaningFreq): 
            # if CleaningFreq is False:
            #     CleaningFreq=100
            BackgroundThread=threading.Thread(
                target=self.__ipcleaner,
                args=(CleaningFreq,),
                daemon=True)
            BackgroundThread.start()
        
        return self.__Validator(ip=IP_Adrs)

        
    def __Fileopener(self)->int:
        if getattr(self, "__isfileopen", False):
            return 0
        data=dict()
        fullpath=self.fullpath
        try:
            with open (fullpath,'r') as File:
                try:
                    self.CurrentFile = open(fullpath, 'r+')
                    self.Data=json.load(File)
                    return 1
                except  json.JSONDecodeError as error:
                    # self.Data={self.ip:[int(time.time()),1]}
                    # self.Data[self.ip]={
                    #     "Time":int(time.time()),
                    #     "Count":1}
                    return 0

                except FileNotFoundError as Fnf:
                    print("EEroro")
                    return self.__Filedumper(operation=0)
        except FileNotFoundError as Fnf:

            return self.__Filedumper(operation=0)

        except FileExistsError as FEE:

             return 0
        except Exception as error:
 
            print(error)
            return 0
    def __Filedumper(self,operation=0,Data=None)->int:
        fullpath=self.fullpath
        flag=0
        if self.CurrentFile is None:
            self.CurrentFile = open(fullpath, 'w')    
        try:
            self.CurrentFile.seek(0)
            json.dump(Data,self.CurrentFile,indent=4)
            self.CurrentFile.truncate()
            self.CurrentFile.flush()
            flag=1
            
        except Exception as e:
            try :
                with open("LOg..txt",'a') as file:
                    record=f"{time.time()}:Error is {e}\n"
                    file.write(record)
                    
                flag=0
            except Exception as err:
                flag=0
        if operation==1:               
                self.CurrentFile.close()
                __isfileopen=False
                return 1
        else:
            return flag

            
                            
        pass           
    def __Validator(self,ip:int)->int:
        currenttime=int(time.time())
        lastseen=currenttime-self.Data[ip]["Time"]
        self.Data[ip]["Time"]=currenttime
        flag=1
        if lastseen>self.Metrics["Cooldowntime"]:
            if ((self.Data[ip]["Count"]>self.Metrics["AllowedFreq"])):
                self.Data[ip]["Count"]=0
                flag= 0
        else:
            if (self.Data[ip]["Count"]>self.Metrics["AllowedFreq"]):
                    self.Data[ip]["Count"]=0
            else:
                self.Data[ip]["Count"]=self.Data[ip]["Count"]+1
                flag= 1
            self.__Filedumper(Data=self.Data)
            return flag

            
            
    def __ipcleaner(self,ClnFrq=100):
        self.thread_running=True
        while True:
            pass
            
        






if __name__=="__main__":
    t=RateLimiter("3232235781")
    t.API_RL("3232235781")
    
        # self.Data[self.ip]={
        #                 "Time":int(time.time()),
        #                 "Count":1}
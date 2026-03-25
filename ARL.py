import os
import sys
from pathlib import Path
import json
import time
import threading
# import ipaddress


class RateLimiter:
    __isfileopen :bool = False
    __samplefile = Path(sys.modules['__main__'].__file__).stem
    def __init__(self,filename=__samplefile,filetype="json",folder=None):
        self.thread_running = False
        self.filename=filename 
        self.filetype=filetype
        self.Data=dict()
        self.CurrentFile=None
        self.lock = threading.RLock()
        self.stop_event = threading.Event()
        self.fullpath=os.path.join(folder or "", f"{filename}.{filetype}")
        self.Validopen=self.__Fileopener()

        pass
    def API_RL(self,IP_Adrs:str,Cleaning=False,
               CooldownTime=20,AllowedFreq=8,MinAttempts=10,CleaningFreq=8,ResetTime=8,Sleeptime=8
               ):
        # if isinstance(ipaddress,str):
        #     self.ip=int(ipaddress.ip_address(IP_Adrs))
        # else:print("Here")
        #     self.ip=IP_Adrs
        self.Metrics={
            "Cooldowntime":CooldownTime,
            "AllowedFreq":AllowedFreq,
            "MinAttempts":MinAttempts }
        # background_thread = threading.Thread(target=self.hehe, args=(start_val,), daemon=True)
        if Cleaning and not self.thread_running:
            self.thread_running=True
            BackgroundThread=threading.Thread(
            
                target=self.__ipcleaner,
                args=(CleaningFreq,ResetTime,),
                daemon=False)
            BackgroundThread.start()
            
        return self.__Validator(ip=IP_Adrs,CoolDown=Sleeptime)
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
                    self.__isfileopen=True
                    return 1
                except  json.JSONDecodeError as error:
                    return 0

                except FileNotFoundError as Fnf:

                    return self.__Filedumper(operation=0)
        except FileNotFoundError as Fnf:
                self.CurrentFile=open(fullpath, 'w')
                # print("HAHHA")
                # json.dump({},self.CurrentFile,indent=4)
                return 1
            # return self.__Filedumper(operation=0)

        except FileExistsError as FEE:

             return 0
        except Exception as error:
 
            print(error)
            return 0
    def __Filedumper(self,operation=0,Data=None)->int:
        # print(Data)
        # if msg is not None: print(msg[0])
        try:  
            with self.lock:
                # if msg is not None: print(msg[1])    
                fullpath=self.fullpath
                flag=0
                
                if Data is None:
                    Data={}
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
                        self.__isfileopen=False
                        return 1
                else:
                    self.__isfileopen=True
                    return flag
        except Exception as e:
            print("HEHEH")

            
                            
        pass           
    def __Validator(self,ip:int,CoolDown=8)->int:

            currenttime=int(time.time())
            error=False
            flag=1
            with self.lock:  
                try:
                    lastseen=currenttime-self.Data[ip]["LastSeenTime"]
                except KeyError:

                    self.Data[ip]={
                        "WindowTime":currenttime,
                        "LastSeenTime":currenttime,
                        "Visits":1   
                    }
                    error=True
                self.Data[ip]["Time"]=currenttime
                if  error is False:
                    if lastseen>self.Metrics["Cooldowntime"]:
                        
                            self.Data[ip]["Visits"]=1
                            flag= 1
                    else:
                        if (self.Data[ip]["Visits"]>=self.Metrics["AllowedFreq"]):
                                flag=0
                                self.Data[ip]["Visits"]=0
                                
                        else:
                            self.Data[ip]["Visits"] += 1
                            flag= 1                
                self.__Filedumper(Data=self.Data)
                if flag==0:
                    time.sleep(CoolDown)
                    flag=1
                    
                    
                return (flag or error)   



    def __ipcleaner(self,ClnFrq=10,restlimit=8):
        
        self.thread_running=True
        CleanData={}
        while not self.stop_event.is_set():
            # print("Inside the Loop")
            self.stop_event.wait(ClnFrq)
            if self.stop_event.is_set():
                break
            with self.lock:
                # print("Inside the Lock")
                currenttime=int(time.time())
                # Keystodelete=[]
                changes=False
                CleanData=self.Data.copy()
                keys=list(CleanData.keys())
                for ip in keys:
                    # print("Checking IPs")
                    # print("Key here")
                    if(currenttime-CleanData[ip]["LastSeenTime"]>restlimit):
                        # print("BYEEE")
                        # Keystodelete.append(ip)
                        # print("Found IP")
                        changes=True
                        try:
                            del CleanData[ip]
                        except Exception as e:
                            print(e)
                if changes is True:
                    # print("Bye IPPPP")
                    self.Data=CleanData
                    self.__Filedumper(Data=self.Data)
                    changes=False
                # print("Sleep")

            # print("Loop End")
            time.sleep(ClnFrq)
        self.thread_running = False 
                    
            
if __name__=="__main__":
    t=RateLimiter()
    v=t.API_RL("127.0.0.2",Cleaning=True,CleaningFreq=1,CooldownTime=7)
    print(v)

            
        





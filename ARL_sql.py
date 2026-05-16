import os
import sys
from pathlib import Path
import json
import time
import threading
import copy
import sqlite3


class __RateLimiter:
    __isfileopen :bool = False
    __samplefile = Path(sys.modules['__main__'].__file__).stem
    def __init__(self,filename=__samplefile,filetype="db",folder=None):
        self.thread_running = False
        self.filename=filename 
        self.filetype=filetype
        self.Data=dict()
        self.CurrentFile=None
        self.lock = threading.RLock()
        self.stop_event = threading.Event()
        self.fullpath=os.path.join(folder or "", f"{filename}.{filetype}")
        self.cursor=None
        self.connection=None
        self.Validopen=self.__Fileopener()
        self.AutoUpdate=False
        pass
    def API_RL(self,IP_Adrs:str,Cleaning=False,AutoUpdate=False,
               CooldownTime=20,AllowedFreq=8,CleaningFreq=80,ResetTime=8,
               UpdateFreq=80)->int:
        # if isinstance(ipaddress,str):
        #     self.ip=int(ipaddress.ip_address(IP_Adrs))
        # else:print("Here")
        #     self.ip=IP_Adrs
        self.AutoUpdate=AutoUpdate
        self.Metrics={
            "CooldownTime":CooldownTime,
            "AllowedFreq":AllowedFreq,
           
                 }
        # background_thread = threading.Thread(target=self.hehe, args=(start_val,), daemon=True)
        if (Cleaning or (AutoUpdate)) and not self.thread_running:
            try:
                self.thread_running=True
                BackgroundThread=threading.Thread(
                
                    target=self.__BackgroundWorker,
                    args=(CleaningFreq,ResetTime,UpdateFreq,Cleaning,),
                    daemon=False)
                BackgroundThread.start()
            except Exception as e:
                print("Erro reached")
                Cleaning=False
                AutoUpdate=False
        return self.__Validator(ip=IP_Adrs)
    def __Fileopener(self)->int:
        if getattr(self, "__isfileopen", False):
            return 0
        data=dict()
        fullpath=self.fullpath
        ##Sql implementation here now
        try: 
            self.CurrentFile=f"{self.fullpath}"
            self.__isfileopen=True
            self.connection=sqlite3.connect(self.CurrentFile,check_same_thread=False, 
    timeout=10.0)
            self.cursor=self.connection.cursor()
            self.cursor.execute('''
                        create table if not exists UserIps(
                            IP Text primary key,
                                jsondata TEXT
                                )''') #Table is created 
            self.Data={row[0]: json.loads(row[1]) for row in self.cursor.fetchall()}
            self.__isfileopen=False
            self.connection.commit()
            
        except Exception as e:
            print(e)
            return 0 
        return 1
    def __Filedumper(self,operation=0,Data=None,update=1)->int:
        # print(Data)
        # if msg is not None: print(msg[0])
        if (update & self.AutoUpdate) :
            return 1
        try:  
            with self.lock:
                # if msg is not None: print(msg[1])    
                fullpath=self.fullpath
                flag=0
                
                if Data is None:
                    Data={}
                
                try:
                   #Write the data 
                    for keys,data in self.Data.items():
                        datatodump=json.dumps(data)
                        self.cursor.execute("Insert or replace  into UserIps (IP,jsondata) VALUES (?,?)",(keys,datatodump,))
                        self.connection.commit()
                #    self.connection.close()
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
            with open("LOg..txt",'a') as file:
                        record=f"{time.time()}:Error is {e}\n"
                        file.write(record)

            
                            
        pass           
    def __Validator(self,ip:int)->int:

            currenttime=int(time.time())
            error=False
            flag=1
            with self.lock:  
                try:
                    lastseen=currenttime-self.Data[ip]["LastSeenTime"]
                except KeyError:

                    self.Data[ip]={
                        # "WaitTime":0,
                        "WaitStamp":0,
                        "LastSeenTime":currenttime,
                        "Visits":1   
                    }
                    error=True
                self.Data[ip]["LastSeenTime"]=currenttime
                if  error is False:
                    if lastseen>self.Metrics["CooldownTime"]:
                            # self.Data[ip]["WaitTime"]=0
                            self.Data[ip]["WaitStamp"]=0
                            self.Data[ip]["Visits"]=1
                            flag= 1
                    else:
                        Datacopy=copy.deepcopy(self.Data)
                        self.Data[ip],flag=  self.__RecentVists(Data=Datacopy[ip],CrnTime=currenttime)

                self.__Filedumper(Data=self.Data)                    
                return (flag or error)   
    def __RecentVists(self,Data,CrnTime)->tuple: #Solution For DeadLock
        

        if Data["Visits"]<=self.Metrics["AllowedFreq"]:
            Data["WaitStamp"]=0
            Data["Visits"]+=1
            return (Data,1)
        # timetowait=0
        if Data["WaitStamp"]==0:
            Data["WaitStamp"]=CrnTime+self.Metrics["CooldownTime"]
            Data["Visits"]+=1
            return (Data,self.Metrics["CooldownTime"])
        else:
            timetosend=Data["WaitStamp"]-CrnTime
            Data["Visits"]+=1
            if timetosend<=0:
                Data["WaitStamp"]=0
                Data["Visits"]=0
                timetosend=1
            
            return (Data,timetosend)        
    def __BackgroundWorker(self,ClnFrq=100,restlimit=80,UpdateFreq=80,Cleaning=False):
        
        self.thread_running=True
        CleanData={}
        Slptime=self.__Timecalculator(ClnFrq,UpdateFreq)
        print("Entred Background Worker")
        while not self.stop_event.is_set():
            # print("Inside the Loop")
            self.stop_event.wait(ClnFrq)
            if self.stop_event.is_set():
                break
            #here write about the clenaing freq
            print(Cleaning)
            self.__Filedumper(Data=self.Data,update=0)
            if Cleaning:

                currenttime=int(time.time())
                try:
                    self.cursor.execute("Delete  from UserIps where  ?- LastSeenTime >?",(currenttime,restlimit,))
                    deleted_rows = self.cursor.fetchall()
                    if deleted_rows:
                        self.connection.commit()
                    with self.lock: 
                        for row in deleted_rows:
                            deleted_ip=row[0]
                            self.Data.pop(deleted_ip,None)
                                                    
                except Exception as e:
                        with open("LOg..txt",'a') as file:
                            record=f"{time.time()}:Error is {e}\n"
                            file.write(record)
                # print("Sleep")
            
            # print("Loop End")
            time.sleep(Slptime)
        self.thread_running = False 
    def __Timecalculator(self,CleaningFrq,UpdateFreq)->int:
        return 2                

__Rl=__RateLimiter()
def Ratelimiter(IP_Adrs:str,Cleaning=False,AutoUpdate=False,
                CooldownTime=20,AllowedFreq=8,CleaningFreq=80,ResetTime=8,UpdateFreq=8,Filename=None,FolderPath=None)->int:
    global __Rl
    if (Filename is not None) and (FolderPath is not None):
        __Rl = __RateLimiter(filename=Filename, folder=FolderPath)
    
# def API_RL(self,IP_Adrs:str,Cleaning=False,AutoUpdate=False,
#                CooldownTime=20,AllowedFreq=8,CleaningFreq=80,ResetTime=8,
#                UpdateFreq=80)
    
    return (__Rl.API_RL(IP_Adrs=IP_Adrs,Cleaning=Cleaning,AutoUpdate=AutoUpdate,
               CooldownTime=CooldownTime,AllowedFreq=AllowedFreq,CleaningFreq=CleaningFreq,ResetTime=ResetTime,UpdateFreq=UpdateFreq))

            
if __name__=="__main__":

    
    v=Ratelimiter("127.0.0.2",Cleaning=0,CleaningFreq=1,CooldownTime=7)
    print(v)

            
        





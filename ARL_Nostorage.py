import time
import threading



class __RateLimiter:
   
    def __init__(self):
        self.thread_running = False       
        self.Data=dict()
        self.stop_event = threading.Event()
        self.lock = threading.RLock()

        pass
    def API_RL(self,IP_Adrs:str,Cleaning=False,CleaningFreq=80,CooldownTime=80,AllowedFreq=10,ResetTime=100)->int:
        # if isinstance(ipaddress,str):
        #     self.ip=int(ipaddress.ip_address(IP_Adrs))
        # else:print("Here")
        self.Metrics={
            "CooldownTime":CooldownTime,
            "AllowedFreq":AllowedFreq}
        if (Cleaning ) and not self.thread_running:
            self.thread_running=True
            BackgroundThread=threading.Thread(
            
                target=self.__BackgroundWorker,
                args=(CleaningFreq,ResetTime,),
                daemon=True)
            BackgroundThread.start()
            
        return self.__Validator(ip=IP_Adrs)
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
                        self.Data[ip],flag=  self.__RecentVists(Data=self.Data[ip],CrnTime=currenttime)

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
    def __BackgroundWorker(self,ClnFrq=100,restlimit=100):
        
        self.thread_running=True
        self.Data={}
        
        while not self.stop_event.is_set():
            # print("Inside the Loop")
                # self.stop_event.wait(ClnFrq)
                if self.stop_event.is_set():
                    break
           
                with self.lock:
                    # print("Inside the Lock")
                    currenttime=int(time.time())
                    # Keystodelete=[]
                    changes=False
                    keys=list(self.Data.keys())
                    for ip in keys:
                        # print("Checking IPs")
                        # print("Key here")
                        if(currenttime-self.Data[ip]["LastSeenTime"]>restlimit):
                            # print("BYEEE")
                            # Keystodelete.append(ip)
                            # print("Found IP")
                            changes=True
                            try:
                                del self.Data[ip]
                            except Exception as e:
                                print(e)
                    if changes is True:
                        # print("Bye IPPPP")
                        self.Data=self.Data
                        changes=False
            
                # print("Sleep")

            # print("Loop End")
                time.sleep(ClnFrq)
        self.thread_running = False 
               

__Rl=__RateLimiter()
def Ratelimiter(IP_Adrs:str,Cleaning=False,CleaningFreq=80,AllowedFreq=10,ResetTime=100,Cooldowntime=20)->int:
    global __Rl
   
    
    return (__Rl.API_RL(IP_Adrs=IP_Adrs,Cleaning=Cleaning,CleaningFreq=CleaningFreq,
                        AllowedFreq=AllowedFreq,ResetTime=ResetTime,CooldownTime=Cooldowntime))

            
            
if __name__=="__main__":

    
    v=Ratelimiter("127.0.0.2",Cleaning=0,CleaningFreq=1)
    print(v)

            
        





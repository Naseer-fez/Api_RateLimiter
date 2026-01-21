
from datetime import datetime
import json
import time
import threading
from functools import wraps











class Api_Limit():
    def __init__(self,filename):
        self.__Fileopener(filename)
        self.filen=filename
        
        self.allips=dict()
        pass
    def __Fileopener(self,filena):
        filename=filena
        if(filena==None):
            filename=self.filen
        try:  
            with open(filename, 'r') as file:
                    self.allips = json.load(file)
        except FileNotFoundError:
            raise Exception(f"Warning: '{filename}' not found. Starting with an empty dictionary.")
    def __Filedumper(self,filena,data):
        filename=filena
        if(filena==None):
            filename=self.filen
        try:
              with open(filename,'w') as file:
                   json.dump(data, file, indent=4)
        except Exception as e:
             raise Exception(f"The following error is {e}")    
    def cleaner(self,lock,required,filename='ips.json'):
        if(required):
            while True:
                time.sleep(20)
                with lock:
                    if(self.clear_ips(self.allips)):
                        self.__Filedumper(filename,self.allips)               
    def clear_ips(self,allips):
            fmt = "%H:%M:%S"
            allips=self.allips
            currenttime=datetime.now().strftime(fmt)
            allowed_freq=2
            allowed_time=20
            keys_to_delete=[]
            for ip in allips:
                prevtime=allips[ip][0]
                freq=allips[ip][1]
                t1 = datetime.strptime(currenttime, fmt)
                t2 = datetime.strptime(prevtime, fmt)
                diff = (t1 - t2).total_seconds()

                if(diff<allowed_time):
                    keys_to_delete.append(ip)
            for ip in keys_to_delete:
                del allips[ip]
            return len(keys_to_delete) > 0    
    def ratelimiter(self,ip,filena=None):
        filename=filena
        if(filena==None):
            filename=self.filen
        
        self.__Fileopener(filena=filename)
        fmt = "%H:%M:%S"
        currenttime=datetime.now().strftime(fmt)
        if ip not in self.allips:
            self.allips[ip]=[currenttime,1]
            self.__Filedumper(filena=filename, data=self.allips)
            return "Done"
        prevtime=self.allips[ip][0]
        freq=self.allips[ip][1]
        
        t1 = datetime.strptime(currenttime, fmt)
        t2 = datetime.strptime(prevtime, fmt)
        diff = (t1 - t2).total_seconds()
        freqattempts=5
        if freq>=freqattempts:
            attempts=5
            if(diff>attempts):
                self.allips[ip]=[currenttime,2]
                self.__Filedumper(filena=filename, data=self.allips)
                return "Done"
            if(diff<attempts):
                # self.allips[ip]=[currenttime,freq-1]
                # self.__Filedumper(filena=filename, data=self.allips)
                return f"{(attempts-diff)}"
            
        self.allips[ip]=[currenttime,freq+1]
        self.__Filedumper(filena=filename, data=self.allips)
        
        return "Done"
    def ipcleaner(self,filena=None,required=None):
        filename=filena
        if(filena==None):
            filename=self.filen
        if(required):
            data_lock = threading.Lock()
            thread = threading.Thread(
                target=self.cleaner, 
                args=(data_lock, required, filename)
            )
            thread.daemon = True
            thread.start()
            
        

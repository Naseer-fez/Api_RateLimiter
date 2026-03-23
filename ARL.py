import os
import sys
from pathlib import Path
import json
import time
class RateLimiter:
    __isfileopen :bool = False
    __samplefile = Path(sys.modules['__main__'].__file__).stem
    def __init__(self,ip_adrs,filename=__samplefile,filetype="json"):
        self.ip=ip_adrs
        self.filename=filename
        self.filetype=filetype
        self.Validopen=self.__Fileopener()
        print(self.Validopen)
        pass
    def __Fileopener(self):
        if getattr(self, "__isfileopen", False):
            return 0
        data=dict()
        fullpath=f"{self.filename}.{self.filetype}"
        try:
            with open (fullpath,'r') as File:
                try:
                    self.Data=json.load(File)
                except  json.JSONDecodeError as error:
                    # self.Data={self.ip:[int(time.time()),1]}
                    self.Data[self.ip]={
                        "Time":int(time.time()),
                        "Count":1}
                finally:
                    __isfileopen=True
        except FileNotFoundError as Fnf:
            return self.__Filedumper(operation=0)
 

        except FileExistsError as FEE:

             return 0
        except Exception as error:
            print("HEHEH")
            return 0

    def __Filedumper(self,operation=0):
        fullpath=f"{self.filename}.{self.filetype}"
        self.Data[self.ip]={
                        "Time":int(time.time()),
                        "Count":1}
        try:
            with open(fullpath,'w') as File:
                json.dump(self.Data,File,indent=4)
                return 1
        except json.JSONDecodeError as error:
                return 0
        finally:
            if(operation==1):
                File.close()
                __isfileopen=False
            else:
                File.flush()
                os.fsync(File.fileno())
            
                            
        pass           
if __name__=="__main__":
    t=RateLimiter(12)
    

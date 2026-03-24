def __Validator(self,ip:int)->int:

        currenttime=int(time.time())
        error=False
        CopyData=self.Data.copy()        
        try:
            lastseen=currenttime-CopyData["Time"]
        except KeyError:

            CopyData[ip]={
                "Time":currenttime,
                "Count":1   
            }
            error=True
            


            return 1
        CopyData["Time"]=currenttime
        flag=1
        if lastseen>self.Metrics["Cooldowntime"]:
            if ((CopyData["Count"]>self.Metrics["AllowedFreq"])):
                CopyData["Count"]=0
                flag= 0
        else:
            if (CopyData["Count"]>self.Metrics["AllowedFreq"]):
                    CopyData["Count"]=0
            else:
                CopyData["Count"]=CopyData["Count"]+1
                flag= 1
                
        
        self.__Filedumper(Data=CopyData)

        return (flag or error)   
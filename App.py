from flask import Flask,request
from datetime import datetime

# import asyncio

app=Flask(__name__)

allips=dict()









def iptester(ip):
    fmt = "%H:%M:%S"
    currenttime=datetime.now().strftime(fmt)
    if ip not in allips:
        allips[ip]=[currenttime,1]
        return
    prevtime=allips[ip][0]
    freq=allips[ip][1]
    
    t1 = datetime.strptime(currenttime, fmt)
    t2 = datetime.strptime(prevtime, fmt)
    diff = (t1 - t2).total_seconds()
    freqattempts=5
    if freq==freqattempts:
        attempts=5
        if(diff>attempts):
            allips[ip]=[currenttime,1]
            return
        if(diff<attempts):
            # return "Too Many Attempts"
            raise TypeError(f"{attempts-diff}")
        return
    
    allips[ip]=[currenttime,freq+1]
    

@app.route("/")
def hello_world():
    yourip=request.remote_addr
    try:
        iptester(ip=yourip)
    except Exception as e:
        return f"Too Many Attempts wait for {e} secs  "
    
    

    return f"Your ip address is {yourip}"
    # iptester(ip=yourip)



if __name__=="__main__":
    app.run(debug=True)
    # asyncio.run(clear_ips())
    
        
    
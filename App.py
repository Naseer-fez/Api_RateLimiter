from flask import Flask,request
from datetime import datetime
import json
import threading
import Clear_ip 
# import asyncio

app=Flask(__name__)
allips=dict()
data_lock = threading.Lock()
filename = 'ips.json'
try:
    with open(filename, 'r') as file:
        
        allips = json.load(file)
except FileNotFoundError:
    # raise Exception(f"Warning: '{filename}' not found. Starting with an empty dictionary.")
    pass


def dumper(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


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
            raise TypeError(f"{int(attempts-diff)}")
        return
    
    allips[ip]=[currenttime,freq+1]
    

@app.route("/")
def hello_world():
    yourip=request.remote_addr
    try:
        iptester(ip=yourip)
    except Exception as e:
        return f"Too Many Attempts wait for {(e)} secs \n "
    
    # data=allips[yourip]
    # data=[allips[yourip][0],str(allips[yourip][1])]
    data=dict()
    data[yourip]=[allips[yourip][0],str(allips[yourip][1])]
    dumper(data,filename)
    return f"Your ip address is {yourip}"
    # iptester(ip=yourip)



if __name__=="__main__":
    
    task=Clear_ip.cleaner
    taks_args=[filename,data_lock]
    thread=threading.Thread(target=task,args=taks_args)
    thread.daemon=True
    thread.start()
    app.run(debug=True,use_reloader=False)
    # asyncio.run(clear_ips())
    
        
    
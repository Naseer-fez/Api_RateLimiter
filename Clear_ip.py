from datetime import datetime
import time
import json

allips=dict()
def openjson(filename):
    try:
        with open(filename, 'r') as file:
            
            allips = json.load(file)
    except Exception as e:
        raise Exception ("The File not found")


def dumper(filename):
    with open(filename, 'w') as file:
        json.dump(allips, file, indent=4)


def clear_ips():
    
    fmt = "%H:%M:%S"
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

def cleaner(lock,filename='ips.json'):
    openjson(filename)
    while True:
        
        time.sleep(7)
        
        # clear_ips()
        with lock:
            if(clear_ips()):
                dumper(filename)
        
        raise Exception ("Done")
        
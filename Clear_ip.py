from datetime import datetime
import time

allips=dict()


def clear_ips():
    
    fmt = "%H:%M:%S"
    currenttime=datetime.now().strftime(fmt)
    allowed_freq=2
    allowed_time=20
    all_keys = [key for d in allips for key in d]
    for ip in all_keys:
        prevtime=allips[ip][0]
        freq=allips[ip][1]
        t1 = datetime.strptime(currenttime, fmt)
        t2 = datetime.strptime(prevtime, fmt)
        diff = (t1 - t2).total_seconds()

        if(diff<allowed_time):
            del allips[ip]



while True:
    time.sleep(20)
    clear_ips()
        
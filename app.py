from flask import Flask,request,render_template
from ARL import RateLimiter as Rl
import time
app=Flask(__name__)


@app.route("/",methods=["POST","GET"])
def home():
    ip=request.remote_addr
    v=Rl()
    check=v.API_RL("127.0.0.2",Cleaning=True,CleaningFreq=1,CooldownTime=7)
    # v=t.API_RL("127.0.0.2",Cleaning=True,CleaningFreq=1,CooldownTime=7)
    if check==1:
        return render_template("index.html", Msg=f"Hiii,{ip}")
    else:

        return render_template("index.html", Msg=f"Waitttttttttt for {check}")
    
   



if __name__=="__main__":
    app.run(debug=True)
    # RateLimiter(12)
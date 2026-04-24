from flask import Flask,request,render_template
from ARL import Ratelimiter as Rl
import time
app=Flask(__name__)


@app.route("/",methods=["POST","GET"])
def home():
    ip=request.remote_addr


    Cooldown=int(Rl(ip))
    # v=t.API_RL("127.0.0.2",Cleaning=True,CleaningFreq=1,CooldownTime=7)
    if Cooldown==1:
        return render_template("index.html", Msg=f"Hiii,{ip}")
    else:
        # time.sleep(check)
        # return {"error": "Too many requests", "retry_after": Cooldown}, 429
        return render_template("index.html", Msg=f"You need to wait for {Cooldown}"),429
    # return render_template("index.html", Msg=f"Hiii,{ip}")
   



if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)
    # RateLimiter(12)
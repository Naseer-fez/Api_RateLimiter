from flask import Flask,request,render_template
from ARL import RateLimiter as Rl
import time
app=Flask(__name__)


@app.route("/",methods=["POST","GET"])
def home():
    ip=request.remote_addr
    v=Rl()

    Cooldown=int(v.API_RL("127.0.0.2",Cleaning=False,CooldownTime=7))
    # v=t.API_RL("127.0.0.2",Cleaning=True,CleaningFreq=1,CooldownTime=7)
    if Cooldown==1:
        return render_template("index.html", Msg=f"Hiii,{ip}")
    else:
        # time.sleep(check)
        # return {"error": "Too many requests", "retry_after": Cooldown}, 429
        return render_template("index.html", Msg=f"Hiii,{ip}\nWith tiem lap"),429
    # return render_template("index.html", Msg=f"Hiii,{ip}")
   



if __name__=="__main__":
    app.run(debug=True)
    # RateLimiter(12)
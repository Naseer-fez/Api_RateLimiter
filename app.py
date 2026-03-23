from flask import Flask,request,render_template
from ARL import RateLimiter

app=Flask(__name__)


@app.route("/",methods=["POST","GET"])
def home():
    ip=request.remote_addr
    
    
    
    
    return render_template("index.html", Msg=f"Hiii,{ip}")
    
   



if __name__=="__main__":
    # app.run(debug=True)
    RateLimiter(12)
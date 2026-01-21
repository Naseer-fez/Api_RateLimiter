import Api_Limiter as ap
from flask import Flask, request

app = Flask(__name__)

filename = "ips.json"
limiter = ap.Api_Limit(filename=filename)

@app.route("/")
def hello_world():
    yourip = request.remote_addr
    data = limiter.ratelimiter(ip=yourip,filena=filename)
    
    if data == "Done":
        return f"Your ip address is {yourip}"
    else:
        return f"Too Many Attempts wait for {data} secs \n "

if __name__ == "__main__":
    limiter.ipcleaner(filena=filename, required=True)
    app.run(debug=True, use_reloader=False)
from test import RequiredRateLimiter
from flask import Flask

app=Flask(__name__)


@app.route("/")
@RequiredRateLimiter()
def Home():
    return "HI"

if __name__=="__main":

    app.run()
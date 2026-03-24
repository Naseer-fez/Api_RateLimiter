if __name__=="__main__":
    t=RateLimiter()
    v=t.API_RL("127.0.0.2",Cleaning=True,CleaningFreq=1,CooldownTime=7)
    print(v)
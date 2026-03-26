from ARL import RateLimiter as Rl
import time
import random
import string
random.seed(42)
V=Rl()
users=100000
sample=list()

# for i in range (0,users):
#     result = ''.join(random.choices(string.ascii_letters, k=15))
#     sample.append(result)
sample=["abcdefgh"]*1000
Succ=list()
Fail=list()
fai=0
suc=0
count=0
print("HAAH")
for j in range (0,100):
    for k in range (0,users):
        for i in sample:
            count+=1
            value=V.API_RL(IP_Adrs=f"{i}{count}")
            if value==1:
                suc+=1
                Succ.append(suc)
            else:
                fai+=1
                Fail.append(fai)

        print(f"The Round {k+1}:")
        print(f"Succes :{len(Succ)}")
        Succ.clear()
        print(f"Falure:{len(Fail)}")
        if len(Fail)==100:
            time.sleep(8)
        Fail.clear()
        time.sleep(1)
    
    
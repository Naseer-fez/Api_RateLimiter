##  How to Run
```python
from ARL import ratelimiter as APIRL
#Import the Function

# Checking rate limit for a specific IP
CoolDown=APIRL(IP_Adrs="127.0.0.1", #IP address ofthe Client
#_______________________________________________________________
Cleaning=False, #To Enable the Ip Address  Cleaning 
CleaningFreq=80,# The Frequency at which the cleaning shoudl occur
UpdateFreq=70 #If you want to update the Data only after a certain time to reduce I/O operations(value in sec)
CooldownTime=20, #Amount of time differnce the Clients last vist shoudld 
# exced for the IP address cleaner to remove the data
#    ***  FOR JSON AND SQL Format only     ***
#If passed to "no stograge" option then this arguments will not be passed to the ratelimiter
#_______________________________________________________________
AllowedFreq=8, #The Number of Fair attempts the Client can send the request to the server
ResetTime=8 # After the Client is denied the access , how much time 
#they need to wait to get the access again 
FileName="Test" # The file name to store the data
Format="sql" # The File extenstion type which the ratelimiter is going to use to store the data
# Extensions available are : sql to use sqllite , json to use json format 
# If nothing is mentioned then the data will not be stored
FolderPath="Test" # The path at which u want to store this results

)
if CoolDown == 1: #The Client  can  access the API
    return "You are a Valid user"
else: # the Request is denied 
    return f"You need to wait {CoolDown}"  
   ```
**This is a test code **
### The Code Return 
- 1 : Means the Client Can Access the API
- other than 1: Means the Client Need to wait for the access of the API
___
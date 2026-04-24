# **API RateLimiter V2**

## What is a API Rate Limiter?
### An API(Application Programing Interface) Rate Limiter  is a traffic control component desgined to restrict the number of requests from a client to the server.


## Improvemnts from the Previous Version:

- ### **Better File Handaling:**
####  With the newer version the main problem of the previous version is addresed ,which is the file handling in the previous version the api rate limiter was constantly reading and writing the data on file, this is method was a good method if u have a modern SSD  and can constaly Read and Write data on that.But in most servers Older HDD are a primary source for Storage.

#### **Solution**: Instead on reading the data constaly we only read the data once and we use a Python Dictonary which exist on RAM , which makes it extermely fast to perform operations and then we Write the data
___
- ###  **Secondary Memory Focus**
####  With the Concers or Constant Read and Write the Newer version have the Data stored in the Secondary Memory which makes the Retriaval and updatation of the data ever Faster so that the server can countiously run without any interruption ,with many modern Server racking up very large amount of RAM , this version of the code only uses ram for the IP data stored , so that the rest of the server wont be Bottlenecked with the hge memory over head of the ratelimiter .
___
- ### **Code Modularity**
#### The present version is made with the future improvemnets and the Code Readibilty in the mind , the present version used Conversional Naming Scheams and proper Function rule :- One Function One Task
______
- ### **Code Abstraction**
#### This version utilizes abstraction to simplify user interaction. By consolidating all features into a single primary function—acting as a 'main gateway'—the implementation becomes intuitive. This allows users to deploy the rate limiter effectively without needing to navigate the complexities of the underlying codebase.
_____
##  How to Run
```python
from ARL import Ratelimiter as APIRL
#Import the Function

# Checking rate limit for a specific IP
CoolDown=APIRL(IP_Adrs="127.0.0.1", #IP address ofthe Client
Cleaning=False, #To Enable the Ip Address  Cleaning 
CleaningFreq=80,# The Frequency at which the cleaning shoudl occur
CooldownTime=20, #Amount of time differnce the Clients last vist shoudld 
# exced for the IP address cleaner to remove the data
AllowedFreq=8, #The Number of Fair attempts the Client can send the request to the server
ResetTime=8 # After the Client is denied the access , how much time 
#they need to wait to get the access again 
FileName="Test" # The file name to store the data
FileType=".json" # The File extenstion
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
## Libaries Used:
### 
1. #### Os
2. #### Json
3. #### Pathlib
4. #### Threading
5. #### Time
6. #### copy



## Architecture
___
- ### The Core architecture involves using Threads for the IP Address cleaning , which make sure 2 operations run simunateously and even if the main thread dies the IP Address Cleaner thread is still going to run so that it can clear up the unused IPS for saving the memory for the both Primary and the Secondary.
- ### With the help of the private function the user can only access one valid function which is usefull reducing unexpected error.
- ### The Data is Stored in a Json file, which reduces the complexity of high performance centraic Systems and can eaily be read by the Developers.
```json
{   #Ip address 
  "127.0.0.2": {
    "WaitStamp": 0, #The amout of time the Client have to wait for the access of the server 
    "LastSeenTime": 1774536998, #The last request of the Client to the server
    "Visits": 1 #THe number of times the client visited the server 
    # Range is (1 ,AllowedFreq)
  }
}
```
- ### The main Idelogy of this project is to reduce the complexity for the developers so that they can focus completely on developing the code rather than the security  aspect of the server

## Advice
---
### A Using of the Decorator is recomended as this reduces the boiler plate code and make the flow of the code easier to understand and also make sure the bugs have a root file to debug.
### A samll Decorator Example is Given But, that is for Flask Implementation Depening on your API Framework You need to change the Code , A small Line chnage depening on your FrameWork will do the job 

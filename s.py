from jsonrpcserver import Success, method, serve
from jsonrpcclient import request, parse

import requests
import base64

import sys
import os
import subprocess

if len(sys.argv) > 1:
    serverNumber = sys.argv[1]

else:
    print("sorry you forgot to add a server number... shutting down")
    quit()

myFriends = list()

def getFunctionWithoutParam(portToCall, function):
    try:
        response = requests.post(f"http://localhost:{portToCall}/", json=request(function))
        parsed = parse(response.json())

        print(parsed.result)

        return parsed.result

    except:
        print(" ----- Are you sure that port and function exist?" + serverNumber + function)

        return False

def getFunctionWithParam(portToCall, function, params):
    try:
        response = requests.post(f"http://localhost:{portToCall}/", json=request(function, params=params))
        parsed = parse(response.json())

        print(parsed.result)

        return parsed.result

    except:
        print(" ----- Are you sure that port and function exist?" + serverNumber + function)

        return False

@method
def ping():
    return Success("pong")

@method
def whoareyou():
    return Success(f"Server Number: {serverNumber} Port Number: 500{serverNumber}")

@method
def make_folder(folder_name):
    try: 
        os.mkdir(folder_name)
        return Success(f"Folder {folder_name} created")
    except:
        return Success(f"Folder {folder_name} already exists")

@method
def delete_folder(folder_name):
    try:
        os.rmdir(folder_name)
        return Success(f"Folder {folder_name} deleted")
    except:
        return Success(f"Folder {folder_name} does not exist")
    
@method
def get_version():
    result = subprocess.run(["py", "--version"], capture_output=True, text=True)
    finalResultOutout = result.stdout
    return Success(f"Python version: {finalResultOutout}")

@method
def search(file_name):
    if os.path.isfile(file_name):
        return Success(f"File {file_name} exists")
    else:
        return Success(f"File {file_name} does not exist")
    
@method
def add_friend(friend):
    myFriends.append(friend)
    return Success(f"Friend {friend} added")

@method
def online(friends):
    myFriends.extend(friends) # this prints the friends it should, but then doesnt add them to the global variable
    sent_from = friends[0]
    for friend in myFriends:
        if friend != sent_from:
            getFunctionWithParam("500" + friend, "add_friend", {"friend": serverNumber})
    return Success(f"Online signal sent")

@method
def offline():
    for friend in myFriends:
        getFunctionWithParam("500" + friend, "remove_friend", {"friend": serverNumber})

    return Success(f"Offline signal sent")

@method
def startup(server_num):
    if server_num in myFriends:
        return Success(f"Server {server_num} already running")
    
    os.system(f'start /b py s.py {server_num} &')
    getFunctionWithParam("500" + server_num, "online", {"friends": [serverNumber] + myFriends})
    myFriends.append(server_num)
    return Success(f"Server {server_num} started")

@method
def shutdown():
    offline()
    quit() # try catch caught this as an error, so it didnt run, meaning server kept running
    return Success(f"Server {serverNumber} shutdown")

@method
def get_friends():
    return Success(f"Server {serverNumber} has friends: {myFriends}")

@method
def remove_friend(friend):
    print(friend + "  " + serverNumber)
    myFriends.remove(friend)
    return Success(f"Friend {friend} removed")

@method
def heart_beat():
    responded = list()
    for friend in myFriends:
        response = getFunctionWithoutParam("500" + friend, "ping")
        if response:
            responded.append(friend)

    return Success(f"Sent from {serverNumber} Response from: {responded}")

@method
def pass_msg(target, servers): # change to pass list of targets?
    servers.remove(serverNumber)
    if serverNumber == target:
        return Success("Message received")
    elif len(servers) != 0:
        print("Message passed to " + servers[0])
        response = getFunctionWithParam("500" + servers[0], "pass_msg", {"target": target, "servers": servers})
        if response == "Message received":
            return Success(response)
        
    return Success("Server not found")
        


if __name__ == "__main__":
    print(f"server number {serverNumber} running.....")
    portNumber = '500' + serverNumber
    serve(port=int(portNumber))
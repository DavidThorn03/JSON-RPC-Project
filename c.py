from jsonrpcclient import request, parse, Ok

import requests
import base64

def getInput(message):
    print(message)
    return input()

def getServer():
    server = getInput(f"Please enter the server number {serverList}: ")
    try:
        #if server not in serverList:
        #    print(" ----- Server not found")
        #    return getServer()
        return int(server) + 5000
    except:
        print(" ----- Please enter a valid number")
        return getServer()

def getFunctionWithoutParam(portToCall, function):
    try:
        response = requests.post(f"http://localhost:{portToCall}/", json=request(function))
        parsed = parse(response.json())

        print(parsed.result)

        return parsed.result

    except:
        print(" ----- Are you sure that port and function exist?")

        return False

def getFunctionWithParam(portToCall, function, params):
    try:
        response = requests.post(f"http://localhost:{portToCall}/", json=request(function, params=params))
        parsed = parse(response.json())

        print(parsed.result)

        return parsed.result

    except:
        print(" ----- Are you sure that port and function exist?")

        return False
    
serverList = list()

def ping():
    portToCall = getServer()

    getFunctionWithoutParam(portToCall, "ping")

def make_folder():
    portToCall = getServer()
    folder_name = getInput("Please enter the folder name: ")

    getFunctionWithParam(portToCall, "make_folder", {"folder_name": folder_name})


def delete_folder():
    portToCall = getServer()
    folder_name = getInput("Please enter the folder name: ")

    getFunctionWithParam(portToCall, "delete_folder", {"folder_name": folder_name})


def whoareyou():
    portToCall = getServer()

    getFunctionWithoutParam(portToCall, "whoareyou")

def get_version():
    portToCall = getServer()

    getFunctionWithoutParam(portToCall, "get_version")

def search():
    portToCall = getServer()
    file_name = getInput("Please enter the file name: ")

    getFunctionWithParam(portToCall, "search", {"file_name": file_name})

def startup():
    server_num = getInput("Enter the sever number you want to start")

    started = getFunctionWithParam("500" + serverList[0], "startup", {"server_num": server_num})

    if started == "Server " + server_num + " started":
        serverList.append(server_num)

def shutdown():
    server_num = getServer()

    getFunctionWithoutParam(server_num, "shutdown")
    serverList.remove(str(server_num - 5000))

def get_friends():
    portToCall = getServer()

    getFunctionWithoutParam(portToCall, "get_friends")

def heart_beat():
    getFunctionWithoutParam("500" + serverList[0], "heart_beat")


def pass_msg():
    target = getInput("Please enter the server you want to pass the message too: ")

    getFunctionWithParam("500" + serverList[0], "pass_msg", {"target": target, "servers": serverList})



if __name__ == "__main__":
    print("Welcome!")

    #add logic to query for active servers
    serverList.append("1")

    while True:

        print("please type a menu option")

        print("1. make folder")
        print("2. delete folder")
        print("3. who are you")
        print("4. get version")
        print("5. search")
        print("6. startup")
        print("7. shutdown")
        print("8. get friends")
        print("9. heart beat")
        print("10. pass message")
        print("11. remove server")
        print("12. ping")

        option = int(input())

        if option == 1:
            make_folder()

        elif option == 2:
            delete_folder()

        elif option == 3:
            whoareyou()
        
        elif option == 4:
            get_version()
        
        elif option == 5:
            search()

        elif option == 6:
            startup()

        elif option == 7:
            shutdown()
        
        elif option == 8:
            get_friends()
        
        elif option == 9:
            heart_beat()

        elif option == 10:
            pass_msg()

        elif option == 11:
            server_num = getServer()

            serverList.remove(server_num)

        elif option == 12:
            ping()

        else: 
            print(" ----- Please enter a valid option")
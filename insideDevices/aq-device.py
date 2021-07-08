import json
from connection import *
import connection
from datetime import datetime

state = 0


def getIncomingCommands():
    global state
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", 5006))
    while True:
        if connection.CONNECTED:
            data, addr = sock.recvfrom(1024)
            print(data)
            try:
                jsonParsed = json.loads(data)
                SN = jsonParsed['SN']
                if SN == connection.SERIAL_NUMBER:
                    state = jsonParsed['state']
            except Exception as e:
                pass
        else:
            sleep(1)


def sendData():
    global i
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        if connection.CONNECTED:
            sock.sendto(
                bytes(
                    "{\"SN\": \"" + SERIAL_NUMBER + "\",\"nickname\":\"" +
                    connection.NICKNAME + "\",\"action\": \"AQ\",\"power\":" +
                    str(connection.POWER) + ", \"value\":" + str(state) + "}",
                    "utf-8"), ("255.255.255.255", 5005))
            print("{\"SN\": \"" + SERIAL_NUMBER + "\",\"nickname\":\"" +
                  connection.NICKNAME + "\",\"action\": \"AQ\",\"power\":" +
                  str(connection.POWER) + ", \"value\":" + str(state) + "}")
            print("state=" + str(state))
        sleep(5)


checkConnection = threading.Thread(target=waitForConnection)
sender = threading.Thread(target=sendData)
getCommands = threading.Thread(target=getIncomingCommands)

checkConnection.start()
sender.start()
getCommands.start()

while True:
    sleep(1)

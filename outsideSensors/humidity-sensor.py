from connection import *
import connection, threading, socket
from datetime import datetime

value = -1

humidityTimes = {}

with open(SOURCE_FILE, mode='r+') as csv_file:
    for row in csv_file:
        if (row.split(',')[3] == '\n'):
            humidityTimes[row.split(',')[1]] = 'error'
            continue
        humidityTimes[row.split(',')[1]] = row.split(',')[3]


def parseTemp(text):
    res = ""
    for i in text:
        if i.isnumeric() or i == '.' or i == '-':
            res += i
    return float(res)


def findInitialValue():
    global value
    foundFirst = False
    initialTime = datetime.strptime(datetime.now().strftime("%#H:%M:%S"),
                                    "%H:%M:%S")
    for time in humidityTimes:
        if humidityTimes[time] != "error":
            temp = datetime.strptime(time, "%H:%M:%S")
            if foundFirst:
                if (temp > initialTime):
                    break
                else:
                    value = parseTemp(humidityTimes[time])
            else:
                if temp < initialTime:
                    foundFirst = True


def getValue():
    global value
    while (True):
        try:
            time = datetime.now().strftime("%#H:%M:%S")
            newValue = humidityTimes[time]
            if newValue != "error":
                value = parseTemp(newValue)
        except:
            pass
        sleep(1)


def sendData():
    global i
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        if connection.CONNECTED:
            if value != -1:
                sock.sendto(
                    bytes(
                        "{\"SN\": \"" + SERIAL_NUMBER + "\",\"nickname\":\"" +
                        connection.NICKNAME +
                        "\",\"measure\": \"HUM\", \"value\":" + str(value) +
                        "}", "utf-8"), ("255.255.255.255", 5005))
                print("{\"SN\": \"" + SERIAL_NUMBER + "\",\"nickname\":\"" +
                      connection.NICKNAME +
                      "\",\"measure\": \"HUM\", \"value\":" + str(value) + "}")
        sleep(5)


findInitialValue()

checkConnection = threading.Thread(target=waitForConnection)
sender = threading.Thread(target=sendData)
getData = threading.Thread(target=getValue)

getData.start()
checkConnection.start()
sender.start()

while True:
    sleep(1)

import string, random, os
from time import sleep

FAKE_SSID = "WirelessRouter"
FAKE_PASSWORD = "Router123"
FILENAME = "\insideSensors\insideCold.csv"
SOURCE_FILE = os.getcwd() + FILENAME

SERIAL_NUMBER_SEED = string.ascii_letters + string.digits

CONNECTED = False
SERIAL_NUMBER = ""
DEBUGING = True
HOST = '255.255.255.255'
PORT = 5005
NICKNAME = ""


def generateSerialNumber():
    global SERIAL_NUMBER
    for i in range(10):
        SERIAL_NUMBER += random.choice(SERIAL_NUMBER_SEED)


generateSerialNumber()
print("(Outside device) serial number: " + SERIAL_NUMBER)


def waitForConnection():
    global CONNECTED, NICKNAME
    while True:
        if not CONNECTED:
            ssid = str(input("Enter ssid: "))
            password = str(input("Enter password: "))
            NICKNAME = str(input("Enter sensor nickname: "))
            if ssid == FAKE_SSID and password == FAKE_PASSWORD:
                CONNECTED = True
                print("Succesfully connected to wireless network!")
                print("Sending data started...")
            else:
                print("Wrong ssid or password!")
                continue
        sleep(5)

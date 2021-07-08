from time import sleep
from typing import Counter
from dbService.api import get_outside_sensors_data, get_room_count_open_windows, get_room_devices, get_rooms, get_turn_off_room_devices
import itertools, socket, windowScoreCalculator

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


def assignDevicesToRooms(allRooms, allDevices):
    for i in allRooms:
        for j in allDevices:
            if i.belongsToDevice(j.id):
                i.devices.append(j)


def startDevice(serialNumber):

    sock.sendto(
        bytes("{\"SN\":\"" + serialNumber + "\",\"state\":1}", "utf-8"),
        ("255.255.255.255", 5006))


def stopDevice(serialNumber):
    sock.sendto(
        bytes("{\"SN\":\"" + serialNumber + "\",\"state\":0}", "utf-8"),
        ("255.255.255.255", 5006))


def startDevices(devices, tag, id):
    toTurnOff = get_turn_off_room_devices(devices, tag, id)
    for i in devices.devices:
        startDevice(i.serialNumber)
    for i in toTurnOff:
        stopDevice(i)


class DeviceCombination:
    def __init__(self, devices, value):
        self.devices = devices
        self.value = value


def get_outside_temp_average(sensors):
    HUM = None
    TEMP = None
    AQ = None
    AQcounter = 0
    TEMPcounter = 0
    HUMcounter = 0
    for i in sensors:
        if i[1] == "AQ":
            if AQ is None:
                AQ = i[0]
            else:
                AQ += i[0]
            AQcounter += 1
        if i[1] == "TEMP":
            if TEMP is None:
                TEMP = i[0]
            else:
                TEMP += i[0]
            TEMPcounter += 1
        if i[1] == "HUM":
            if HUM is None:
                HUM = i[0]
            else:
                HUM += i[0]
            HUMcounter += 1
    if HUMcounter != 0:
        HUM = HUM / HUMcounter
    if TEMPcounter != 0:
        TEMP = TEMP / TEMPcounter
    if AQcounter != 0:
        AQ = AQ / AQcounter
    return (TEMP, HUM, AQ)


def getCombinationPoints(combination):
    val = 0
    for i in combination:
        val += i.capabilities['power']
    return val


def getAllCombinations(devices):
    result = []
    for i in range(1, len(devices) + 1):
        temp = list(itertools.combinations(devices, i))
        for j in temp:
            result.append(j)
    return result


def turnOffCounterDevices(devices):
    for i in devices:
        stopDevice(i.serialNumber)


def getDevicesToStart(devices, currentTemp, desiredTemp, economyFactor,
                      curentPowerFactor, requiredPowerFactor, tagComparator,
                      id):
    if (tagComparator[0] +
            tagComparator[1]) == 'DE' or tagComparator == 'COOL':
        if currentTemp <= desiredTemp:
            turnOffCounterDevices(devices)
            return
    else:
        if currentTemp >= desiredTemp:
            turnOffCounterDevices(devices)
            return

    comfort = 10 - economyFactor
    tempDifference = abs(currentTemp - desiredTemp)
    tempDifferenceFactor = -1
    if comfort > 0:
        tempDifferenceFactor = tempDifference * comfort / economyFactor
    else:
        tempDifferenceFactor = tempDifference / economyFactor
    if tempDifferenceFactor >= 1:
        difference = curentPowerFactor - requiredPowerFactor
        comfort = 10 - economyFactor
        if difference > 0:
            if comfort > 0:
                difference = difference * comfort / economyFactor
                min = -1
                for i in devices:
                    if min == -1:
                        min = i
                    else:
                        if min.value < difference:
                            if i.value > min.value:
                                min = i
                        elif i.value >= difference and i.value < min.value:
                            min = i
                startDevices(min, tagComparator, id)
            else:
                for i in devices:
                    stopDevice(i.serialNumber)
        else:
            difference = difference * comfort / economyFactor
            min = -1

            allCombinations = []
            for i in getAllCombinations(devices):
                allCombinations.append(
                    DeviceCombination(i, getCombinationPoints(i)))
            for i in allCombinations:
                if min == -1:
                    min = i
                else:
                    if i.value < abs(difference):
                        if i.value > min.value:
                            min = i
                        else:
                            continue
                    else:
                        if min.value < abs(difference):
                            min = i
                        else:
                            if i.value < min.value:
                                min = i
            startDevices(min, tagComparator, id)

    else:
        for i in devices:
            stopDevice(i.serialNumber)


def getTagDevices(tag, list):
    res = []
    for i in list:
        if i.capabilities['action'] == tag:
            res.append(i)
    return res


def processAllRooms(data):
    outside = get_outside_temp_average(get_outside_sensors_data())
    outsideTemp = outside[0]
    outsideHum = outside[1]
    outsideAQ = outside[2]

    for i in data:
        window = windowScoreCalculator.getWindowsDesirability(
            windowScoreCalculator.getDesirabilityTemperature(
                i.temperature, i.targetTemperature, outsideTemp),
            windowScoreCalculator.getDesirabilityHumidity(
                i.humidity,
                i.targetHumidity,
                outsideHum,
            ),
            windowScoreCalculator.getDesirabilityAirQuality(
                i.airQuality, i.targetAirQuality, outsideAQ))
        windowsPowerFactor = 0
        if window >= 0:
            for j in i.devices:
                if j.capabilities['action'] == "WINDOW":
                    startDevice(j.serialNumber)
            windowsPowerFactor = get_room_count_open_windows(i.id) * 200
        else:
            for j in i.devices:
                if j.capabilities['action'] == "WINDOW":
                    stopDevice(j.serialNumber)

        if i.canDecide():
            heatDevices = getTagDevices("HEAT", i.devices)
            humidityDevices = getTagDevices("HUM", i.devices)
            dehumidityDevices = getTagDevices("DEHUM", i.devices)
            coolingDevices = getTagDevices("COOL", i.devices)
            airQualityDevices = getTagDevices("AQ", i.devices)
            if i.temperature is not None and len(heatDevices) > 0:
                getDevicesToStart(heatDevices, i.temperature,
                                  i.targetTemperature, i.objectiveSpeed,
                                  windowsPowerFactor, 3000, 'HEAT', i.id)
            if i.temperature is not None and len(coolingDevices) > 0:
                getDevicesToStart(coolingDevices, i.temperature,
                                  i.targetTemperature, i.objectiveSpeed,
                                  windowsPowerFactor, 3000, 'COOL', i.id)
            if i.humidity is not None and len(humidityDevices) > 0:
                getDevicesToStart(humidityDevices, i.humidity,
                                  i.targetHumidity, i.objectiveSpeed,
                                  windowsPowerFactor, 3000, 'HUM', i.id)
            if i.humidity is not None and len(dehumidityDevices) > 0:
                getDevicesToStart(dehumidityDevices, i.humidity,
                                  i.targetHumidity, i.objectiveSpeed,
                                  windowsPowerFactor, 3000, 'DEHUM', i.id)
            if i.airQuality is not None and len(airQualityDevices) > 0:
                getDevicesToStart(airQualityDevices, i.airQuality,
                                  i.targetAirQuality, i.objectiveSpeed,
                                  windowsPowerFactor, 3000, 'AQ', i.id)


def AIDecider():
    while True:
        try:
            allRooms = get_rooms()
            allDevices = get_room_devices()
            assignDevicesToRooms(allRooms, allDevices)
            processAllRooms(allRooms)
        except Exception as e:
            print("AI error -> " + str(e))
        finally:
            sleep(10)

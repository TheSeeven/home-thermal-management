class Room:
    def __init__(self, id, temperature, humidity, airQuality, objectiveSpeed,
                 targetTemperature, targetHumidity, targetAirQuality):
        self.id = id
        self.temperature = temperature
        self.humidity = humidity
        self.airQuality = airQuality
        self.objectiveSpeed = objectiveSpeed
        self.targetTemperature = targetTemperature
        self.targetHumidity = targetHumidity
        self.targetAirQuality = targetAirQuality
        self.devices = []

    def belongsToDevice(self, id):
        if self.id == id:
            return True
        return False

    def canDecide(self):
        if len(self.devices) > 0:
            return True


class Device:
    def __init__(self, id, serialNumber, capabilities):
        self.id = id
        self.serialNumber = serialNumber
        self.capabilities = capabilities
        self.power = capabilities['power']

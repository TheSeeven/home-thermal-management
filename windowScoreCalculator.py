TEMPERATURE_BIAS = 0.30
AIR_QUALITY_BIAS = 0.65
HUMIDITY_BIAS = 0.05


def getDesirabilityAirQuality(inside, desired, outside):
    if inside == None or desired == None or outside == None:
        return 0
    result = outside - inside

    isOutsideBetter = outside > inside
    isInsideOk = inside >= desired

    if isOutsideBetter and isInsideOk:
        return 0
    elif isOutsideBetter and not isInsideOk:
        return result * 2
    elif not isOutsideBetter and isInsideOk:
        return 0
    elif not isOutsideBetter and not isInsideOk:
        return result * 2


def getDesirabilityTemperature(inside, desired, outside):
    result = 0
    if inside == None or desired == None or outside == None:
        return result
    isOutsideHotter = outside > inside
    isInsideTooHot = inside > desired

    if isInsideTooHot and not isOutsideHotter:
        if not outside > desired:
            result = abs(outside - inside) + abs(inside - desired)
        else:
            if inside != outside:
                result = abs(outside - desired)
            else:
                result = -abs(outside - desired)

    elif isInsideTooHot and isOutsideHotter:
        result = -abs(outside - desired) + -abs(outside - inside)
    elif not isInsideTooHot and isOutsideHotter:
        if inside != desired:
            result = abs(outside - inside) + abs(desired - inside)
        else:
            result = -abs(outside - desired)
    elif not isInsideTooHot and not isOutsideHotter:
        result = -abs(desired - outside) + -abs(outside - inside)
    return result


def getDesirabilityHumidity(inside, desired, outside):
    result = 0

    if inside == None or desired == None or outside == None:
        return result
    isOutsideMoreHumid = outside > inside
    isInsideTooHumid = inside > desired

    if isInsideTooHumid and isOutsideMoreHumid:
        result = -abs(outside - desired) + -abs(outside - desired)

    elif not isInsideTooHumid and isOutsideMoreHumid:
        if inside != desired:
            result = abs(outside - inside) + abs(desired - inside)
        else:
            result = -abs(outside - desired)
    elif not isInsideTooHumid and not isOutsideMoreHumid:
        result = -abs(desired - outside) + -abs(outside - inside)
    elif isInsideTooHumid and not isOutsideMoreHumid:
        if not outside > desired:
            result = abs(outside - inside) + abs(inside - desired)
        else:
            if inside != outside:
                result = abs(outside - desired)
            else:
                result = -abs(outside - desired)
    return result


def getWindowsDesirability(temperatureFactor, humidityFactor, aqFactor):
    temp = (temperatureFactor / 10) * TEMPERATURE_BIAS
    hum = (humidityFactor / 20) * HUMIDITY_BIAS
    aq = aqFactor * AIR_QUALITY_BIAS
    return temp + hum + aq

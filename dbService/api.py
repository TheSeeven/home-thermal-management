import sqlite3
import json, time
from dbService.classes import *
from dbService.tables_data import *
from dbService.devtools import *
from dbService.exceptions import *

DATABASE_LINK = 'home-thermal-database.db'


def enableForeignKey(connection):
    connection.execute("PRAGMA foreign_keys = 1")


# database initialization
def createDatabaseAndTables():
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            enableForeignKey(DB)

            for table in DB_TABLES:
                try:
                    DB.execute(table.getQuerry())
                    DB.commit()
                    if table.name == "room":
                        DB.execute(
                            "INSERT INTO 'room' ('id','nickname','temperature','humidity','airQuality','objectiveSpeed') VALUES (-1,'',NULL,NULL,NULL,NULL)"
                        )
                        DB.commit()
                    log("Table {name} created".format(name=table.name))
                except Exception as e:
                    log("Error creating table {name} with error: {err}".format(
                        name=table.name, err=str(e)))
            log("Database created")
    except Exception as e:
        log("Error creating database: " + str(e))


# database interface
class interface:
    class post:
        @staticmethod
        def insert_room(params):
            paramsLength = len(params)
            if paramsLength != 5:
                return (
                    '1',
                    str(
                        ParameterError(
                            "Invalid number of parameters! Only 5 accepted ({number} were given)"
                            .format(number=paramsLength))))
            nickname = params[0]
            temperature = params[1]
            humidity = params[2]
            airQuality = params[3]
            objectiveSpeed = params[4]

            def func(nickname, temperature, humidity, airQuality,
                     objectiveSpeed):
                with sqlite3.connect(DATABASE_LINK) as DB:
                    enableForeignKey(DB)

                    def getRoomId():
                        cursor = DB.cursor()
                        cursor.execute("""SELECT seq
                            FROM sqlite_sequence
                            WHERE name = 'room'""")
                        try:
                            result = cursor.fetchall()[0][0] + 1
                        except:
                            result = 1
                        finally:
                            cursor.close()
                            return result

                    id = str(getRoomId())
                    DB.execute(
                        """INSERT INTO 'room' ('id','nickname','temperature','humidity','airQuality','objectiveSpeed') VALUES ({id},'{nickname}',{temperature},{humidity},{airQuality},{objectiveSpeed})"""
                        .format(id=id,
                                temperature=str(temperature),
                                humidity=str(humidity),
                                airQuality=str(airQuality),
                                objectiveSpeed=str(objectiveSpeed),
                                nickname=str(nickname)))
                    DB.execute(
                        """INSERT INTO 'sensor_data' ('id') VALUES ('{id}')""".
                        format(id=id))
                    DB.commit()
                    log("Room inserted succesfully!")

            try:
                func(nickname, temperature, humidity, airQuality,
                     objectiveSpeed)
                return ('0', "Room added!")
            except Exception as e:
                log("Room insert failed: " + str(e))
                return ('1', str(InsertError("Error inserting room")))

        @staticmethod
        def update_room(params):

            paramsLength = len(params)
            if paramsLength != 6:
                return (
                    '1',
                    str(
                        ParameterError(
                            "Invalid number of parameters! Only 6 accepted ({number} were given)"
                            .format(number=paramsLength))))
            id = params[0]
            nickname = params[1]
            temperature = params[2]
            humidity = params[3]
            airQuality = params[4]
            objectiveSpeed = params[5]

            def func(id, nickname, temperature, humidity, airQuality,
                     objectiveSpeed):
                with sqlite3.connect(DATABASE_LINK) as DB:
                    enableForeignKey(DB)
                    DB.execute(
                        """UPDATE 'room' SET nickname='{nickname}',temperature={temperature},humidity={humidity},airQuality={airQuality},objectiveSpeed={objectiveSpeed} where id={id}"""
                        .format(id=id,
                                nickname=nickname,
                                temperature=str(temperature),
                                humidity=str(humidity),
                                airQuality=str(airQuality),
                                objectiveSpeed=str(objectiveSpeed)))
                    DB.commit()
                #log("Room with id:{id} update succesfuly!".format(id=id))

            try:
                func(id, nickname, temperature, humidity, airQuality,
                     objectiveSpeed)
                return ('0', "Room settings updated!")
            except Exception as e:
                log("Room with id:{id} update failed: ".format(id=id) + str(e))
                return (
                    '1',
                    str(
                        InsertError(
                            "Failed to change nickname. Nickname '{nickname}' Already exist!"
                            .format(nickname=nickname))))

        @staticmethod
        def delete_room(params):

            paramsLength = len(params)
            if paramsLength != 1:
                return (
                    '1',
                    str(
                        ParameterError(
                            "Invalid number of parameters! Only 1 accepted ({number} were given)"
                            .format(number=paramsLength))))
            id = params[0]

            def func(id):
                with sqlite3.connect(DATABASE_LINK) as DB:
                    enableForeignKey(DB)
                    DB.execute(
                        """DELETE FROM 'room' WHERE id={id}""".format(id=id))
                    DB.commit()

            try:
                func(id)
                log("Room with id:{id} deleted".format(id=id))
                return ('0', "Room deleted succesfully!")
            except Exception as e:
                log("Delete room failed: " + str(e))
                return (
                    '1',
                    str(
                        DeleteError(
                            "Failed to remove room, please refresh the page!"))
                )

        @staticmethod
        def assign_sensor(params):

            paramsLength = len(params)
            if paramsLength != 2:
                return (
                    '1',
                    str(
                        ParameterError(
                            "Invalid number of parameters! Only 2 accepted ({number} were given)"
                            .format(number=paramsLength))))
            newId = params[0]
            serialNumber = params[1]

            def func(newId, serialNumber):
                with sqlite3.connect(DATABASE_LINK) as DB:
                    enableForeignKey(DB)
                    res = """UPDATE 'device' SET id={newId} WHERE device.serialNumber = '{SN}'""".format(
                        newId=str(newId), SN=str(serialNumber))
                    DB.execute(res)

            try:
                func(newId, serialNumber)
                #log("""Device {serialNumber} assigned to id {newId}""".format(
                #    serialNumber=str(serialNumber), newId=str(newId)))
                return ('0', "Device assigned!")
            except Exception as e:
                log("""Failed to assign id {newId} to device {serialNumber}: """
                    + str(e).format(serialNumber=str(serialNumber),
                                    newId=str(newId)))
                return (
                    '1',
                    str(
                        UpdateError(
                            "Error unpairing the sensor, please refresh the page!"
                        )))

    class get:
        @staticmethod
        def get_room_preferences(params):

            paramsLength = len(params)
            if paramsLength != 1:
                return (
                    '1',
                    str(
                        ParameterError(
                            "Invalid number of parameters! Only 1 accepted ({number} were given)"
                            .format(number=paramsLength))))
            id = params[0]

            def func(id):
                with sqlite3.connect(DATABASE_LINK) as DB:
                    enableForeignKey(DB)
                    cursor = DB.cursor()
                    cursor.execute(
                        """SELECT temperature,humidity,airQuality,objectiveSpeed,nickname from room where room.id={id}"""
                        .format(id=str(id)))
                    res = cursor.fetchall()
                    cursor.close()
                    return res[0]

            try:
                return ('0', func(id))
            except Exception as e:
                print(e)
                return ('1', "Room settings not found!")

        @staticmethod
        def get_rooms():
            try:
                with sqlite3.connect(DATABASE_LINK) as DB:
                    enableForeignKey(DB)
                    cursorRoom = DB.cursor()
                    cursorDevice = DB.cursor()

                    cursorRoom.execute(
                        """SELECT room.id, room.nickname, room.temperature, room.humidity, room.airQuality, room.objectiveSpeed, sensor_data.temperature,sensor_data.humidity,sensor_data.airQuality
                    FROM 'room' INNER JOIN 'sensor_data' ON room.id=sensor_data.id AND room.id!=-1"""
                    )

                    cursorDevice.execute("""SELECT *
                        FROM 'device' where id >-1 """)

                    result = (cursorRoom.fetchall(), cursorDevice.fetchall())
                    cursorRoom.close()
                    cursorDevice.close()
                    #log("Rooms retrieved succesfully!")
                    return ('0', result)
            except Exception as e:
                log("Retrieve rooms failed: " + str(e))
                return (
                    '1',
                    str(
                        GetError(
                            "Error retrieving data, refresh the page then please retry"
                        )))

        @staticmethod
        def get_unassigned_devices():
            try:
                with sqlite3.connect(DATABASE_LINK) as DB:
                    enableForeignKey(DB)
                    cursor = DB.cursor()
                    cursor.execute(
                        """SELECT * FROM 'device' WHERE id is NULL""")
                    result = cursor.fetchall()
                    cursor.close()
                    #log("Unpaired devices retrieved succesfully!")
                    return ('0', result)
            except Exception as e:
                log("Retrieve unpaired devices failed: " + str(e))
                return (
                    '1',
                    str(
                        GetError(
                            "Error retrieving data, refresh the page then please retry"
                        )))

        @staticmethod
        def get_outside_sensors():
            try:
                with sqlite3.connect(DATABASE_LINK) as DB:
                    enableForeignKey(DB)
                    cursor = DB.cursor()
                    cursor.execute("""SELECT * FROM 'device' WHERE id = -1""")
                    result = cursor.fetchall()
                    cursor.close()
                    #log("Outside sensors retrieved succesfully!")
                    return ('0', result)
            except Exception as e:
                log("Retrieve outside sensors failed!" + str(e))
                return (
                    '1',
                    str(
                        GetError(
                            "Error retrieving data, refresh the page then please retry"
                        )))


def insert_past_sensor_data():
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            enableForeignKey(DB)
            DB.execute(
                """INSERT INTO 'past_sensor_data' ('id','temperature','humidity','airQuality') SELECT id,temperature,humidity,airQuality FROM 'sensor_data'"""
            )
            DB.commit()
            #log("Past sensor data inserted succesfully")
    except Exception as e:
        log("Past sensor data insert failed: " + str(e))


def update_sensor_data(SN, value):
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            enableForeignKey(DB)
            DB.execute(
                """UPDATE 'device' SET curentValue = {val}, lastUpdate = datetime() WHERE serialNumber='{serialNumber}';"""
                .format(val=str(value), serialNumber=SN))
            DB.commit()
            #log("Data updated succesfully")
    except Exception as e:
        log("Device data update failed: " + str(e))


def insert_new_sensor(SN, deviceType, attribute, value, nickname):
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            enableForeignKey(DB)
            DB.execute(
                "INSERT INTO 'device'('id','nickname','serialNumber','curentValue','capabilities','lastUpdate') VALUES (NULL,'{nick}','{serialNumber}',{value},'{capabilities}',{curdate})"
                .format(nick=nickname,
                        serialNumber=SN,
                        value=str(value),
                        capabilities="{\"" + deviceType + "\":\"" + attribute +
                        "\"}",
                        curdate="datetime()"))
            DB.commit()
            #log("Device inserted succesfully")
    except Exception as e:
        log("Device insert failed: " + str(e))


def insert_new_device(SN, deviceType, attribute, value, power, nickname):
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            enableForeignKey(DB)
            DB.execute(
                "INSERT INTO 'device'('id','nickname','serialNumber','curentValue','capabilities','lastUpdate') VALUES (NULL,'{nick}','{serialNumber1}',{value},'{capabilities}',{curdate})"
                .format(nick=nickname,
                        serialNumber1=SN,
                        value=str(value),
                        capabilities="{\"" + deviceType + "\":\"" + attribute +
                        "\",\"power\":" + str(power) + "}",
                        curdate="datetime()"))
            DB.commit()
            #log("Device inserted succesfully")
    except Exception as e:
        log("Device insert failed: " + str(e))


def device_exists(SN):
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            enableForeignKey(DB)
            cursor = DB.cursor()
            cursor.execute(
                """SELECT count() FROM device WHERE serialNumber='{serialNumber}'"""
                .format(serialNumber=SN))
            result = cursor.fetchall()
            cursor.close()
            #log("Device found succesfully")
            if result[0][0] == 1:
                return True
    except Exception as e:
        log("Error finding device: " + str(e))
    return False


def get_rooms():
    res = []
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            enableForeignKey(DB)
            cursor = DB.cursor()
            cursor.execute(
                "SELECT room.id,room.temperature,room.humidity,room.airQuality,room.objectiveSpeed,sensor_data.temperature,sensor_data.humidity,sensor_data.airQuality FROM 'room' inner join 'sensor_data' on 'room'.id='sensor_data'.id WHERE room.id>-1"
            )
            result = cursor.fetchall()
            cursor.close()
            for i in result:
                res.append(
                    Room(
                        i[0],
                        i[5],
                        i[6],
                        i[7],
                        i[4],
                        i[1],
                        i[2],
                        i[3],
                    ))
            #log("Rooms retrieved succesfully")
    except Exception as e:
        log("Error retrieving devices: " + str(e))
    return res


def get_room_count_open_windows(roomid):
    res = []
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            enableForeignKey(DB)
            cursor = DB.cursor()
            cursor.execute(
                "SELECT count() from device where id={ID} and capabilities like '%window%'"
                .format(ID=str(roomid)))
            res = cursor.fetchall()[0][0]
            cursor.close()
            #log("Windows count retrieved succesfully")
    except Exception as e:
        log("Error retrieving windows count: " + str(e))
    return res


def get_room_devices():
    res = []
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            enableForeignKey(DB)
            cursor = DB.cursor()
            cursor.execute(
                "SELECT id,serialNumber,capabilities FROM device WHERE id is not NULL and id > 0 and capabilities like '%action%'"
            )
            result = cursor.fetchall()
            cursor.close()
            for i in result:
                res.append(Device(i[0], i[1], json.loads(i[2])))
            #log("Room devices retrieved succesfully")
    except Exception as e:
        log("Error retrieving room devices: " + str(e))
    return res


def get_outside_sensors_data():
    res = []
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            enableForeignKey(DB)
            cursor = DB.cursor()
            cursor.execute(
                "SELECT curentValue,capabilities FROM device WHERE id =-1 and curentValue != 'NULL' and capabilities like '%measure%' "
            )
            result = cursor.fetchall()
            cursor.close()
            for i in result:
                res.append((i[0], json.loads(i[1])['measure']))
            #log("Outside sensors retrieved succesfully")
    except Exception as e:
        log("Error retrieving outside sensors: " + str(e))
    return res


def get_turn_off_room_devices(devices, tag, id):
    toNotSelect = ""
    for i in devices.devices:
        toNotSelect += "OR '" + i.serialNumber + "' "
    toNotSelect = toNotSelect.removeprefix("OR ")

    querry = "select serialNumber from device where (device.serialNumber != {notSelect}) AND capabilities like '%{theTag}%' AND capabilities like'%action%' AND id={ID}".format(
        notSelect=toNotSelect, theTag=tag, ID=str(id))
    devices = []
    with sqlite3.connect(DATABASE_LINK) as DB:
        cursor = DB.cursor()
        cursor.execute(querry)
        result = cursor.fetchall()
        cursor.close()
        for i in result:
            devices.append(i[0])
    return devices


def set_room_sensor_data():
    while True:
        allSensors = []
        allRooms = []
        getSensorsQuerry = "SELECT id,curentValue,capabilities FROM device where id>-1 AND capabilities like '%measure%'"
        getRoomsQuerry = "SELECT id FROM room where id>-1"
        with sqlite3.connect(DATABASE_LINK) as DB:
            cursorSensors = DB.cursor()
            cursorRooms = DB.cursor()
            cursorSensors.execute(getSensorsQuerry)
            resSensors = cursorSensors.fetchall()
            cursorSensors.close()
            cursorRooms.execute(getRoomsQuerry)
            resRooms = cursorRooms.fetchall()
            cursorRooms.close()

            for i in resRooms:
                allRooms.append(i)
            for i in resSensors:
                allSensors.append(i)

        result = []
        for i in allRooms:
            temperature = 0.0
            humidity = 0.0
            airQuality = 0.0
            temperatureCounter = 0
            humidityCounter = 0
            airQualityCounter = 0
            for j in allSensors:
                if j[0] == i[0]:
                    if "HUM" in j[2]:
                        humidity += j[1]
                        humidityCounter += 1
                    elif "TEMP" in j[2]:
                        temperature += j[1]
                        temperatureCounter += 1
                    elif "AQ" in j[2]:
                        airQuality += j[1]
                        airQualityCounter += 1
            if temperatureCounter != 0:
                temperature = temperature / temperatureCounter
            else:
                temperature = "NULL"

            if humidityCounter != 0:
                humidity = humidity / humidityCounter
            else:
                humidity = "NULL"
            if airQualityCounter != 0:
                airQuality = airQuality / airQualityCounter
            else:
                airQuality = "NULL"
            result.append((i[0], temperature, humidity, airQuality))

        with sqlite3.connect(DATABASE_LINK) as DB:
            enableForeignKey(DB)
            for i in result:
                querry = "UPDATE sensor_data SET temperature = {temperature},humidity={humidity},airQuality={airQuality} where id={ID}".format(
                    temperature=str(i[1]),
                    humidity=str(i[2]),
                    airQuality=str(i[3]),
                    ID=str(i[0]))
                DB.execute(querry)
                DB.commit()
        time.sleep(5)


def initialize_database():
    createDatabaseAndTables()

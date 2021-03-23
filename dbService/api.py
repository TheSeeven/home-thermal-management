import sqlite3
from dbService.tables_data import *
from dbService.devtools import *
from dbService.exceptions import *



DATABASE_LINK = 'home-thermal-database.db'

# database initialization
def createDatabaseAndTables():
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            log("Database created")
            for table in DB_TABLES:
                try:
                    DB.execute(table.getQuerry())
                    log("Table {name} created".format(name=table.name))
                except Exception as e:
                    log("Error creating table {name} with error: {err}".format(name=table.name, err=str(e)))
    except Exception as e:
        log("Error creating database: " + str(e))

# database interface
class interface:
    @staticmethod
    def insert_room(params):
        paramsLength = len(params)
        if paramsLength != 6:
            return ('1',str(ParameterError("Invalid number of parameters! Only 6 accepted ({number} were given)".format(number=paramsLength))))
        nickname = params[0]
        temperature = params[1]
        humidity = params[2]
        lux = params[3]
        airQuality = params[4]
        objectiveSpeed = params[5] 
        def func(nickname, temperature, humidity, lux, airQuality, objectiveSpeed):
            with sqlite3.connect(DATABASE_LINK) as DB:
                def getRoomId():
                    cursor = DB.cursor()
                    cursor.execute("""SELECT seq
                        FROM sqlite_sequence
                        WHERE name = 'room'""")
                    try:
                        result = cursor.fetchall()[0][0]+1
                    except:
                        result = 1
                    finally:
                        cursor.close()
                        return result
                id = getRoomId()
                DB.execute("""INSERT INTO 'settings' ('id','temperature','humidity','lux','airQuality','objectiveSpeed') VALUES ({id},{temperature},{humidity},{lux},{airQuality},{objectiveSpeed})""".format(
                    id=str(id), temperature=str(temperature), lux=str(lux), humidity=str(humidity), airQuality=str(airQuality), objectiveSpeed=str(objectiveSpeed)))
                DB.execute(
                    """INSERT INTO 'sensor_data' ('id') VALUES ('{id}')""".format(id=id))
                DB.execute("""INSERT INTO 'room' ('nickname') VALUES ('{nickname}')""".format(
                    nickname=nickname))
                DB.commit()
                log("Room inserted succesfully!")
        try:
            func(nickname,temperature,humidity,lux,airQuality,objectiveSpeed)
            return ('0', "Room added!")
        except Exception as e:
            log("Room insert failed: " + str(e))
            return ('1',str(InsertError("Error inserting room")))

   
    @staticmethod
    def insert_device(params):
        paramsLength = len(params)
        if paramsLength != 1:
            return ('1', str(ParameterError("Invalid number of parameters! Only 1 accepted ({number} were given)".format(number=paramsLength))))
        serialNumber = params[0]
        def func(serialNumber):
            with sqlite3.connect(DATABASE_LINK) as DB:
                DB.execute("""INSERT INTO 'sensor' ('serialNumber') VALUES ({serialNumber})""".format(
                    serialNumber=serialNumber))
                DB.commit()
                log("Sensor inser succesfully {SN}".format(SN=serialNumber))
        try:
            func(serialNumber)
            log("Sensor insert succesfully!")
            return ('0', "Sensor with serial number {SN} inserted succesfully!".format(SN=serialNumber))
        except Exception as e:
            log("Insert sensor error: " + str(e))
        
    @staticmethod
    def update_room(params):
        id = params[0]
        nickname = params[1]
        paramsLength = len(params)
        if paramsLength != 2:
            return ('1', str(ParameterError("Invalid number of parameters! Only 2 accepted ({number} were given)".format(number=paramsLength))))
        def func(id, nickname):
            with sqlite3.connect(DATABASE_LINK) as DB:
                DB.execute("""UPDATE 'room' SET nickname='{nickname}' where id={id}""".format(
                    id=id, nickname=nickname))
                DB.commit()
            log("Room with id:{id} update succesfuly!".format(id=id))
        try:
            func(id,nickname)
            return ('0',"Room settings updated!")
        except Exception as e:
            log("Room with id:{id} update failed: ".format(id=id) + str(e))
            return('1',str(InsertError("Failed to change nickname. Nickname '{nickname}' Already exist!".format(nickname=nickname))))

    

    @staticmethod
    def update_room_settings(params):
        id = params[0]
        temperature = params[1]
        humidity = params[2]
        lux = params[3]
        airQuality = params[4]
        objectiveSpeed = params[5]
        paramsLength = len(params)
        if paramsLength != 6:
            return ('1', str(ParameterError("Invalid number of parameters! Only 6 accepted ({number} were given)".format(number=paramsLength))))
        def func(id, temperature, humidity, lux, airQuality, objectiveSpeed):
            with sqlite3.connect(DATABASE_LINK) as DB:
                DB.execute(
                    """UPDATE 'settings' SET temperature={temperature},humidity={humidity},lux={lux},airQuality={airQuality},objectiveSpeed={objectiveSpeed} WHERE id={id}""")
                DB.commit()
        try:
            func(id, temperature, humidity, lux, airQuality, objectiveSpeed)
            return ('0',"Settings updated succesfully!")
        except Exception as e:
            log("Update room with id {id} failed: " + str(e))
            return ('1',str(UpdateError("Failed to update settings for room")))

    @staticmethod
    def delete_room(params):
        id = params[0]
        paramsLength = len(params)
        if paramsLength != 1:
            return ('1', str(ParameterError("Invalid number of parameters! Only 1 accepted ({number} were given)".format(number=paramsLength))))
        def func(id):
            with sqlite3.connect(DATABASE_LINK) as DB:
                DB.execute("""DELETE FROM 'room' WHERE id={id}""".format(id=id))
                DB.commit()
        try:
            func(id)
            log("Room with id:{id} deleted".format(id=id))
            return ('0',"Room deleted succesfully!")
        except Exception as e:
            log("Delete room failed: " + str(e))
            return ('1', str(DeleteError("Failed to remove room, please refresh the page!")))

    @staticmethod
    def delete_device(params):
        id = params[0]
        paramsLength = len(params)
        if paramsLength != 1:
            return ('1', str(ParameterError("Invalid number of parameters! Only 1 accepted ({number} were given)".format(number=paramsLength))))
        def func(id):
            with sqlite3.connect(DATABASE_LINK) as DB:
                DB.execute("""DELETE FROM 'sensor' WHERE id={id}""".format(id=id))
                DB.commit()
        try:
            func(id)
            log("Sensor with id:{id} deleted".format(id=id))
            return ('0',"Sensor upaired!")
        except Exception as e:
            log("Delete sensor failed: " + str(e))
            return ('1', str(DeleteError("Error unpairing the sensor, please refresh the page!")))

    @staticmethod
    def get_rooms():
        try:
            with sqlite3.connect(DATABASE_LINK) as DB:
                cursorRoom = DB.cursor()
                cursorSensors = DB.cursor()

                cursorRoom.execute("""SELECT room.id,room.nickname,settings.temperature,settings.humidity,settings.lux,settings.airQuality,settings.objectiveSpeed,sensor_data.temperature,sensor_data.humidity,sensor_data.lux,sensor_data.airQuality
                FROM 'room' 
                INNER JOIN 'settings' ON room.id=settings.id INNER JOIN 'sensor_data' ON room.id=sensor_data.id""")

                cursorSensors.execute("""SELECT sensor.id,sensor.serialNumber,sensor.nickname,sensor.curentValue
                    FROM 'sensor'""")

                result = (cursorRoom.fetchall(), cursorSensors.fetchall())
                cursorRoom.close()
                cursorSensors.close()
                log("Rooms retrieved succesfully!")
                return ('0',result)
        except Exception as e :
            log("Retrieve rooms failed: " + str(e))
            return ('1',str(GetError("Error retrieving data, refresh the page then please retry")))


def insert_past_sensor_data():
    try:
        with sqlite3.connect(DATABASE_LINK) as DB:
            DB.execute("""INSERT INTO 'past_sensor_data' ('id','temperature','humidity','lux','airQuality') SELECT id,temperature,humidity,lux,airQuality FROM 'sensor_data'""")
            DB.commit()
            log("Past sensor data inserted succesfully")
    except Exception as e:
        log("Past sensor data insert failed: " + str(e))


def update_sensor_data(sensorDataArray):
    def update_sensor():
        pass

    # TODO : LONG IMPLEMENTATION
    pass

def get_past_sensor_data():
    # nu stiu momentan cum trebuie sa iau datele din DB
    pass

def initialize_database():
    createDatabaseAndTables()





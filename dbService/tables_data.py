DB_TABLES = []


class Table:

    insertString = "CREATE TABLE {tableName} ("

    def __init__(self, name, columns):
        self.name = name
        self.columns = columns

    def getQuerry(self):
        res = self.insertString.format(tableName=self.name)
        for columns in self.columns:
            res += columns.getQuerry() + ", "
        res = res[:-2]
        res += ")"
        return res


class Column:
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype

    def getQuerry(self):
        return "{name} {datatype}".format(name=self.name,
                                          datatype=self.datatype)


DB_TABLES.append(
    Table("room", (
        Column("id", "INTEGER UNIQUE NOT NULL"),
        Column("nickname", "TEXT NOT NULL"), Column("temperature", "FLOAT"),
        Column("humidity", "FLOAT"), Column("lux", "FLOAT"),
        Column(
            "airQuality",
            "FLOAT"),
        Column(
            "objectiveSpeed",
            "INTEGER"),
        Column(
            "",
            "FOREIGN KEY ('id') REFERENCES 'room' ('id') ON DELETE CASCADE ON UPDATE CASCADE"
        ))))

DB_TABLES.append(
    Table("sensor_data", (
        Column("id", "INTEGER UNIQUE NOT NULL"), Column(
            "temperature", "FLOAT"), Column("humidity", "FLOAT"),
        Column("lux", "FLOAT"), Column("airQuality", "FLOAT"),
        Column(
            "",
            "FOREIGN KEY ('id') REFERENCES 'room' ('id') ON DELETE CASCADE ON UPDATE CASCADE"
        ))))

DB_TABLES.append(
    Table("past_sensor_data", (
        Column("id", "INTEGER NOT NULL"), Column("temperature", "FLOAT"),
        Column("humidity", "FLOAT"), Column(
            "lux", "FLOAT"), Column("airQuality", "FLOAT"),
        Column("dateTime", "TEXT DEFAULT CURRENT_TIMESTAMP"),
        Column(
            "",
            "FOREIGN KEY ('id') REFERENCES 'room' ('id') ON DELETE CASCADE ON UPDATE CASCADE"
        ))))

DB_TABLES.append(
    Table("device", (
        Column("id", "INTEGER"), Column("serialNumber",
                                        "TEXT NOT NULL UNIQUE"),
        Column("nickname", "TEXT DEFAULT ''"), Column(
            "curentValue", "FLOAT"), Column("capabilities", "JSON NOT NULL"),
        Column(
            "",
            "FOREIGN KEY ('id') REFERENCES 'room' ('id') ON DELETE SET NULL ON UPDATE CASCADE"
        ))))

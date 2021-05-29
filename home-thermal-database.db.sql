BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "room" (
	"id"	INTEGER NOT NULL UNIQUE,
	"nickname"	TEXT NOT NULL,
	"temperature"	FLOAT,
	"humidity"	FLOAT,
	"airQuality"	FLOAT,
	"objectiveSpeed"	INTEGER,
	FOREIGN KEY("id") REFERENCES "room"("id") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "sensor_data" (
	"id"	INTEGER NOT NULL UNIQUE,
	"temperature"	FLOAT,
	"humidity"	FLOAT,
	"airQuality"	FLOAT,
	FOREIGN KEY("id") REFERENCES "room"("id") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "past_sensor_data" (
	"id"	INTEGER NOT NULL,
	"temperature"	FLOAT,
	"humidity"	FLOAT,
	"airQuality"	FLOAT,
	"dateTime"	TEXT DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY("id") REFERENCES "room"("id") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "device" (
	"id"	INTEGER,
	"serialNumber"	TEXT NOT NULL UNIQUE,
	"nickname"	TEXT DEFAULT '',
	"curentValue"	FLOAT,
	"capabilities"	JSON NOT NULL,
	FOREIGN KEY("id") REFERENCES "room"("id") ON DELETE SET NULL ON UPDATE CASCADE
);
INSERT INTO "room" ("id","nickname","temperature","humidity","airQuality","objectiveSpeed") VALUES (0,'',NULL,NULL,NULL,NULL);
INSERT INTO "room" ("id","nickname","temperature","humidity","airQuality","objectiveSpeed") VALUES (-1,'outside',NULL,NULL,NULL,NULL);
INSERT INTO "room" ("id","nickname","temperature","humidity","airQuality","objectiveSpeed") VALUES (1,'kitchen',3.0,4.0,5.0,6);
INSERT INTO "room" ("id","nickname","temperature","humidity","airQuality","objectiveSpeed") VALUES (2,'living',2.0,3.0,4.0,5);
INSERT INTO "sensor_data" ("id","temperature","humidity","airQuality") VALUES (2,5.0,4.0,9.0);
INSERT INTO "sensor_data" ("id","temperature","humidity","airQuality") VALUES (1,2.0,3.0,8.0);
INSERT INTO "device" ("id","serialNumber","nickname","curentValue","capabilities") VALUES (-1,'dsadasdas','',10.0,'{"type":"sensor","measure":"TEMP"}');
INSERT INTO "device" ("id","serialNumber","nickname","curentValue","capabilities") VALUES (-1,'asedrf','',20.0,'{"type":"sensor","measure":"HUM"}');
INSERT INTO "device" ("id","serialNumber","nickname","curentValue","capabilities") VALUES (NULL,'eqweqw','',3.0,'{"type":"sensor","measure":"TEMP"}');
INSERT INTO "device" ("id","serialNumber","nickname","curentValue","capabilities") VALUES (NULL,'errer','',1.0,'{"type":"sensor","measure":"AQ"}');
INSERT INTO "device" ("id","serialNumber","nickname","curentValue","capabilities") VALUES (1,'asdsa','',22.0,'{"type":"sensor","measure":"TEMP"}');
INSERT INTO "device" ("id","serialNumber","nickname","curentValue","capabilities") VALUES (1,'qwerty','',9.0,'{"type":"sensor","measure":"TEMP"}');
INSERT INTO "device" ("id","serialNumber","nickname","curentValue","capabilities") VALUES (2,'cxzcx','',10.0,'{"type":"device","action":"WINDOW"}');
INSERT INTO "device" ("id","serialNumber","nickname","curentValue","capabilities") VALUES (2,'fdsf','',8.0,'{"type":"sensor","measure":"TEMP"}');
COMMIT;

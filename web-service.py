import dbService.api, os, threading, json, socket, threading
from flask import Flask, request, render_template, jsonify
from flask.helpers import make_response, send_from_directory
from flask_cors import CORS
from devtools import *

SERVER_NAME = 'HTM'


class localFlask(Flask):
    def process_response(self, response):
        response.headers['server'] = SERVER_NAME
        return (response)


app = localFlask(__name__,
                 static_url_path="",
                 static_folder="frontend/static",
                 template_folder='frontend/static/html')
app.config['SERVER_NAME'] = 'localhost:5000'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536001

cors = CORS(app)

HUB_SERIAL_NUMBER = "BGDMNG123IOPIGN"


@app.route('/favicon.ico')
def favicon():
    y = os.path.join(app.root_path, "frontend\\static")
    x = send_from_directory(y, 'ico/favicon.ico')
    return x


@app.route('/About', methods=['GET', 'POST'])
def about():
    resp = make_response(render_template("About.html"))
    resp.cache_control.max_age = 179
    return resp


def parseParameters(string):
    res = []
    tempString = ''
    try:
        for char in string:
            if char != ',':
                tempString += char
                continue
            res.append(tempString)
            tempString = ''
        res.append(tempString)
    except:
        return None
    return res


@app.route("/ControlPanel", methods=['GET'])
def controlPanel():
    resp = make_response(render_template("ControlPanel.html"))
    resp.cache_control.max_age = 179
    return resp


@app.route("/api/dbService", methods=['GET', 'POST'])
def api():
    if request.method == "GET" or request.method == "POST":
        function = request.args.get('function')
        parameters = parseParameters(request.args.get('params'))

        result = None
        classAdress = dbService.api.interface
        if request.method == "GET":
            classAdress = classAdress.get
        else:
            classAdress = classAdress.post
        if function is not None:
            try:
                function = getattr(classAdress, function)
            except:
                with open(
                        os.getcwd() +
                        "\\frontend\\static\\html\\406NotAllowed.html",
                        "r") as f:
                    return f.read().replace("{func}", function)
            if parameters:
                result = function(parameters)
            else:
                result = function()
            resp = make_response(
                jsonify({
                    "status": result[0],
                    'data': result[1]
                }))
            resp.mimetype = 'application/js'
            resp.headers['server'] = 'HTM'
            resp.headers['X-Content-Type-Options'] = 'nosniff'
            resp.cache_control.max_age = 1
            return resp
        else:
            with open(
                    os.getcwd() +
                    "\\frontend\\static\\html\\406NotAllowed.html", "r") as f:
                return f.read().replace("{func}", "name")
    else:
        return render_template("405NotAllowed.html")


def handleMessage(message):
    try:
        jsonParsed = json.loads(message)
        SN = jsonParsed['SN']
        value = jsonParsed['value']
        if dbService.api.device_exists(SN):
            dbService.api.update_sensor_data(SN, value)
        else:
            deviceType = ""
            try:
                deviceType = jsonParsed['measure']
                dbService.api.insert_new_sensor(SN, 'measure', deviceType,
                                                value)
            except:
                deviceType = jsonParsed['action']
                dbService.api.insert_new_sensor(SN, 'action', deviceType,
                                                value)
    except Exception as e:
        log("Error updating sensor data: " + str(e))


def listenToDevices():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", 5005))
    while True:
        data, addr = sock.recvfrom(1024)
        handler = threading.Thread(target=handleMessage, args=(data, ))
        handler.start()


if __name__ == "__main__":
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        devicesListenerThread = threading.Thread(target=listenToDevices)
        devicesListenerThread.start()
        dbService.api.initialize_database()
    app.run(debug=True)

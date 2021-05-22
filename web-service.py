import dbService.api, os
from flask import Flask, request, render_template, jsonify
from flask.helpers import send_from_directory
from flask_cors import CORS

app = Flask(__name__,
            static_url_path="",
            static_folder="frontend/static",
            template_folder='frontend/static/html')
cors = CORS(app)

HUB_SERIAL_NUMBER = "BGDMNG123IOPIGN"


@app.route('/favicon.ico')
def favicon():
    y = os.path.join(app.root_path, "frontend\\static")
    x = send_from_directory(y, 'ico/favicon.ico')
    return x


@app.route('/', methods=['GET', 'POST'])
def test():
    return "returnser"


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
    return render_template("ControlPanel.html")


@app.route("/api/dbService", methods=['GET'])
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
            return jsonify({"status": result[0], 'data': result[1]})
        else:
            with open(
                    os.getcwd() +
                    "\\frontend\\static\\html\\406NotAllowed.html", "r") as f:
                return f.read().replace("{func}", "name")
    else:
        return render_template("405NotAllowed.html")


if __name__ == "__main__":
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        dbService.api.initialize_database()
    app.run(debug=True)

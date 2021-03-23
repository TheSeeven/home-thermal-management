import dbService.api, os
from flask import Flask, request
from flask.helpers import send_from_directory

app = Flask(__name__, static_url_path="", static_folder="frontent/static")

HUB_SERIAL_NUMBER = "BGDMNG123IOPIGN"



@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'),'ico/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def test():
  return "tt"

@app.route("/api/dbService",methods=['GET'])
def api():
  if request.method == "GET":
    function = request.args.get('function')
    parameters = request.args.get('params')
    result = None
    def parseParameters(string):
      res = []
      tempString = ''
      try:
        for char in string:
          if char != ',':
            tempString+=char
            continue
          res.append(tempString)
          tempString = ''
        res.append(tempString)
      except:
        return None
      return res
    if function is not None:
      function = getattr(dbService.api.interface, function)
      try:
        result = function(parseParameters(parameters))
      except:
        try:
          result = function()
        except:
          result = ('1',"406 not alowed")
      finally:
        return "{}:{}".format(result[0], result[1])
    return "function does not exst"
  else:
    return "method not allowed"

if __name__ == "__main__":
  if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    dbService.api.initialize_database()
  app.run(debug=True)
  











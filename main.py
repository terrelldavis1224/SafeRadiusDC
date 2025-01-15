import flask
from  crime import *
import pandas as pd
from location import *
import json
from api import *

app = flask.Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        data = flask.request.json

        # Validate content type
        if flask.request.content_type != "application/json":
            return flask.jsonify({"error": "Unsupported Media Type"}), 415

        # Check for address in the request
        if not data or "address" not in data:
            return flask.jsonify({"error": "Invalid request"}), 400

        address = data.get("address")
        
        

        
        Loctions = getLocations(address)

        if Loctions is None:
            return flask.jsonify({"error": "Nothing from location"}), 400
        else:
            map_html,report = update_circle(Loctions[0]["lat"],Loctions[0]["lon"], int(data.get("miles")) , True)  

        return flask.jsonify({'report': report, 'map_html': map_html}), 200

    return flask.render_template("index.html")



@app.route('/map')
def map():
    return update_circle(map_center[0],map_center[1],1,False)[0]


@app.route('/api')
def api():
    return flask.render_template('api.html')


@app.route('/about')
def about():
    return flask.render_template('about.html')



@app.route("/crimes",methods=['GET'])
def get_crimes():

    offense = flask.request.args.get('OFFENSE', default='all')  
    offensegroup = flask.request.args.get('offensegroup', default='all')  
    shift =  flask.request.args.get("SHIFT",default="all")
    processdata=processCrimedata(offense,offensegroup,shift)
    data = processdata.head(10).to_json(orient='records')  
    parsed_data = json.loads(data) 

    return flask.jsonify(parsed_data)

@app.errorhandler(400)
def bad_request(e):
    return flask.jsonify({"error": "Bad Request"}), 400

@app.errorhandler(404)
def not_found(e):
    return flask.jsonify({"error": "Not Found"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return flask.jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)



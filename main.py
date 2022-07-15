# Flask
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from waitress import serve
# Utils
import json
import requests
import datetime
import re
# Token JWT
from flask_jwt_extended import create_access_token, verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# ------------------------- Setting Flask App -------------------------------


app = Flask(__name__)
cors = CORS(app)


# ------------------------- middleware -------------------------------

def format_url():
    parts = request.path.split("/")
    url = request.path
    for part in parts:
        if re.search('\\d', parts):
            url = url.replace(part, "?")
    return url


@app.before_request
def before_request_callback():
    excluded_routes = ["/login"]
    if request.path not in excluded_routes:
        if not verify_jwt_in_request():
            return jsonify({"msg": "Permission denied"}), 401
        # Roles
        user = get_jwt_identity()
        print(user)
        if user["role"] is None:
            return jsonify({"msg": "Permission Denied"}), 401
        else:
            role_id = user["role"]["_id"]
            route = format_url()
            method = request.method
            has_permission = validate_permission(role_id, route, method)
            if not has_permission:
                return jsonify({"msg": "Permission Denied"}), 401


def validate_permission(role_id, route, method):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-security"] + "/permission-role/validate/role/" + role_id
    body = {"url": route, "method": method}
    print(body)
    response = requests.post(url, json=body, headers=headers)
    print(response)
    try:
        data = response.json()
        if "_id" in data:
            return True
    except:
        return False


# ------------------------- Setting JWT Token -------------------------------


def loadFileConfig():
    with open("../ApiGatewayR/config.json") as f:
        data = json.load(f)
    return data


dataConfig = loadFileConfig()

app.config["JWT_SECRET_KEY"] = dataConfig["jwt-key"]
jwt = JWTManager(app)


# ------------------------- Endpoints -------------------------------

@app.route("/resultsbycandidate", methods=["GET"])
def getResultsByCandidate():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/resultsbycandidate"
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/resultsbyparty", methods=["GET"])
def getResultsByParty():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/resultsbyparty"
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/resultsbytable", methods=["GET"])
def getResultsByTable():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/resultsbytable"
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/newsenate", methods=["GET"])
def getNewSenate():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/newsenate"
    response = requests.get(url, headers=headers)
    return response.json()


"""
---------------------------------------------------------------------------
    ENDPOINTS TABLE
---------------------------------------------------------------------------
"""


@app.route("/tables", methods=['GET'])
def get_tables():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/tables"
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/table", methods=['POST'])
def create_table():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/table"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=['GET'])
def get_table(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/tables/" + id
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=['PUT'])
def update_table(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/table/" + id
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=["DELETE"])
def deleteTable(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/table/" + id
    response = requests.get(url, headers=headers)
    return response.json()


"""
---------------------------------------------------------------------------
    ENDPOINTS TABLE
---------------------------------------------------------------------------
"""


@app.route("/partys", methods=["GET"])
def getPartys():
    headers = {"Content-Type": "application/json; chaser=utf-8"}
    url = dataConfig["url-administration"] + "/partys"
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/party/<string:id>", methods=["GET"])
def getParty(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/party/" + id
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/party", methods=["POST"])
def createParty():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/party"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/party/<string:id>", methods=['PUT'])
def updateParty(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/party/" + id
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/party/<string:id>", methods=["DELETE"])
def deleteParty(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/party/" + id
    response = requests.get(url, headers=headers)
    return response.json()


"""
---------------------------------------------------------------------------
    ENDPOINTS CANDIDATES
---------------------------------------------------------------------------
"""


@app.route("/candidates", methods=["GET"])
def getCandidates():
    headers = {"Content-Type": "application/json; chaser=utf-8"}
    url = dataConfig["url-administration"] + "/candidates"
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/candidate/<string:resolution>", methods=["GET"])
def getParty(resolution):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/candidate/" + resolution
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/candidate", methods=["POST"])
def createCandidate():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/candidate"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/candidate/<string:resolution>", methods=['PUT'])
def updateCandidate(resolution):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/candidate/" + resolution
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/candidate/<string:resolution>", methods=["DELETE"])
def deleteCandidate(resolution):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/candidate/" + resolution
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/test", methods=["GET"])
def test():
    return jsonify({"msg": "It works!"})


"""
---------------------------------------------------------------------------
    ENDPOINT TOKEN AND VALIDATION
---------------------------------------------------------------------------
"""


@app.route("/auth", methods=["POST"])
def login():
    # FE -> AGW
    data = request.get_json()
    # AGW -> MS
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-security"] + "/users/validate"
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 401:
        return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401
    elif response.status_code == 500:
        return jsonify({"msg": "Error inesperado"}), 500
    elif response.status_code == 200:
        user = response.json()
        expires = datetime.timedelta(seconds=60 * 60 * 24)
        access_token = create_access_token(identity=user, expires_delta=expires)
        return jsonify({"token": access_token, "user_id": user["_id"]})


"""
---------------------------------------------------------------------------
    ENDPOINTS USERS
---------------------------------------------------------------------------
"""


@app.route("/users/<string:id>", methods=["GET"])
def getUsers():
    headers = {"Content-Type": "application/json; chaser=utf-8"}
    url = dataConfig["url-administration"] + "/users"
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/user/<string:id>", methods=["GET"])
def getUser(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/user/" + id
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/user", methods=["POST"])
def createUser():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/user"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/user/<string:id>", methods=['PUT'])
def updateUser(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/user/" + id
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/user/<string:id>", methods=["DELETE"])
def deleteUser(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/user/" + id
    response = requests.get(url, headers=headers)
    return response.json()


"""
---------------------------------------------------------------------------
    ENDPOINTS USERS
---------------------------------------------------------------------------
"""


@app.route("/rolpermissions", methods=["GET"])
def getRolPermissions():
    headers = {"Content-Type": "application/json; chaser=utf-8"}
    url = dataConfig["url-administration"] + "/rolpermissions"
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/rolpermission/<string:rol>", methods=["GET"])
def getRolPermission(rol):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/rolpermission/" + rol
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/rolpermission/<string:rol>", methods=['PUT'])
def updateRolPermission(rol):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-administration"] + "/rolpermission/" + rol
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


# ------------------------- Server -------------------------------

url = "http://" + dataConfig["url-apigateway"] + ":" + dataConfig["port-apigateway"]
print("Server running: " + url)
serve(app, host=dataConfig["url-apigateway"], port=dataConfig["port-apigateway"])

from flask import Flask
from flask_cors import CORS
from flask import request
import requests
from flask_jwt_extended import verify_jwt_in_request,get_jwt_identity
from flask import jsonify
from waitress import serve
from flask_jwt_extended import JWTManager
import re
from flask import Response
import json
import datetime
from flask_jwt_extended import create_access_token





'''Setting Flask App'''
app = Flask(__name__)
cors = CORS(app)


'''Settings'''
from settings import dataConfig

app.config["JWT_SECRET_KEY"] = dataConfig["jwt-key"]
jwt = JWTManager(app)
url_base = dataConfig["url-administration"]
url_security = dataConfig["url-security"]


''' Middlewares '''


@app.before_request
def before_request_callback():
    print("before_request_callback started")
    excluded_routes = ["/auth"]
    if request.path not in excluded_routes:
        if not verify_jwt_in_request():
            return jsonify({"msg": "Permission denied"}), 401
        # Roles
        user = get_jwt_identity()
        print(user)
        if user["role"] is None:
            return jsonify({"msg": "Permission Denied"}), 401
        else:
            role_id = user["role"]["id"]
            route = format_url()
            method = request.method
            has_permission = validate_permission(role_id, route, method)
            if not has_permission:
                return jsonify({"msg": "Permission Denied"}), 401


def format_url():
    parts = request.path.split("/")
    url = request.path
    for part in parts:
        if re.search('\\d', part):
            url = url.replace(part, "?")
    return url


def validate_permission(role_id, route, method):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-security"] + "/permission-role/validate/role/" + role_id
    body = {"url": route, "metodo": method}
    print(body)
    response = requests.post(url, json=body, headers=headers)
    print(response)
    try:
        data = response.json()
        if "_id" in data:
            return True
    except:
        return False

'''Endpoint Routes'''
headers = {"Content-Type": "application/json; charset=utf-8"}

# >>>>>> Validation

@app.route("/auth", methods=["POST"])
def login():
    # FE -> AGW
    data = request.get_json()
    # AGW -> MS
    url = url_security + "/users/validate"
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


# >>>>> Permissions
@app.route("/permissions/<string:id>", methods=["GET"])
def getPermissionById(id):
    url = url_security + "/permissions/" + id
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/permissions/<string:id>", methods=['PUT'])
def updatePermission(id):
    url = url_security + "/permissions/" + id
    body = request.get_json()
    response = requests.put(url, json=body, headers=headers)
    return response.json()


@app.route("/permissions/<string:id>", methods=["DELETE"])
def deletePermission(id):
    url = url_security + "/permissions/" + id
    response = requests.delete(url, headers=headers)
    if(response.status_code==204):
        return jsonify({"msg": "Permiso eliminado con éxito"}), 204
    return response

# >>>>> Permission Role

@app.route("/permission-role/", methods=["GET"])
def getPermissionRole():
    url = url_security + "/permission-role"
    response = requests.get(url, headers=headers)
    return Response(json.dumps(json.loads(response.content)),  mimetype='application/json')


@app.route("/permission-role/role/<string:id_role>/permission/<string:id_permission>", methods=["POST"])
def createPermissionRole(id_role, id_permission):
    url = url_security + "/permission-role/role/"+id_role +"/permission/"+id_permission
    response = requests.post(url, headers=headers)
    if (response.status_code == 201 or response.status_code==200):
        return jsonify({"msg": "Permiso-rol creado"}), response.status_code
    return response


@app.route("/permission-role/<string:id>", methods=["GET"])
def getPermissionRoleById(id):
    url = url_security + "/permission-role/" + id
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/permission-role/<string:id_pr>/role/<string:id_role>/permission/<string:id_perm>", methods=['PUT'])
def updatePermissionRole(id_pr, id_role, id_perm):
    url = url_security + "/permission-role/" + id_pr + "/role/"+ id_role + "/permission/"+id_perm
    response = requests.put(url, headers=headers)
    return response.json()


@app.route("/permission-role/<string:id>", methods=["DELETE"])
def deletePermissionRole(id):
    url = url_security + "/permission-role/" + id
    response = requests.delete(url, headers=headers)
    if(response.status_code == 200):
        return jsonify({"msg": "Permiso-rol eliminado con éxito"}), response.status_code
    return response

# >>>> Results
@app.route("/candidates-result/", methods=["GET"])
def getAllCandidateResults():
    url = url_base + "/candidates-result"
    response = requests.get(url, headers=headers)
    return Response(json.dumps(json.loads(response.content)),  mimetype='application/json')


@app.route("/parties-result/", methods=["GET"])
def getResultsByParty():
    url = url_base + "/parties-result"
    response = requests.get(url, headers=headers)
    return Response(json.dumps(json.loads(response.content)),  mimetype='application/json')


@app.route("/parties-result/<string:id>", methods=["GET"])
def getResultsByPartyID(id):
    url = url_base + "/parties-result/"+id
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/newsenate/", methods=["GET"])
def getNewSenate():
    url = url_base + "/newsenate"
    response = requests.get(url, headers=headers)
    return response.json()

# >>>> Poll Stations

@app.route("/tables/", methods=['GET'])
def get_tables():
    url = url_base + "/tables"
    response = requests.get(url, headers=headers)
    return Response(json.dumps(json.loads(response.content)),  mimetype='application/json')


@app.route("/table/", methods=['POST'])
def create_table():
    url = url_base + "/table"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=['GET'])
def get_table(id):
    url = url_base + "/table/" + id
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=['PUT'])
def update_table(id):
    url = url_base + "/table/" + id
    body = request.get_json()
    response = requests.put(url, json=body, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=["DELETE"])
def deleteTable(id):
    url = url_base + "/table/" + id
    response = requests.delete(url, headers=headers)
    return response.json()

# >>>> Political Parties

@app.route("/partys/", methods=["GET"])
def getParties():
    url = url_base + "/partys"
    response = requests.get(url, headers=headers)
    return Response(json.dumps(json.loads(response.content)),  mimetype='application/json')

@app.route("/party/<string:id>", methods=["GET"])
def get_party(id):
    url = url_base + "/party/" + id
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/party/", methods=["POST"])
def createParty():
    url = url_base + "/party"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()

@app.route("/party/<string:id>", methods=['PUT'])
def updateParty(id):
    url = url_base + "/party/" + id
    body = request.get_json()
    response = requests.put(url, json=body, headers=headers)
    return response.json()

@app.route("/party/<string:id>", methods=["DELETE"])
def deleteParty(id):
    url = url_base + "/party/" + id
    response = requests.delete(url, headers=headers)
    return response.json()

@app.route("/party/votes/", methods=["GET"])
def getPartyVotes():
    url = url_base + "/party/votes"
    response = requests.get(url, headers=headers)
    return response.json()
# >>>> Candidates

@app.route("/candidates/", methods=["GET"])
def getCandidates():
    url = url_base + "/candidates"
    response = requests.get(url, headers=headers)
    return Response(json.dumps(json.loads(response.content)),  mimetype='application/json')


@app.route("/candidate/<string:resolution>", methods=["GET"])
def getParty(resolution):
    url = url_base + "/candidate/" + resolution
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/candidate/", methods=["POST"])
def createCandidate():
    url = url_base + "/candidate"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/candidate/<string:resolution>", methods=['PUT'])
def updateCandidate(resolution):
    url = url_base + "/candidate/" + resolution
    body = request.get_json()
    response = requests.put(url, json=body, headers=headers)
    return response.json()


@app.route("/candidate/<string:resolution>", methods=["DELETE"])
def deleteCandidate(resolution):
    url = url_base + "/candidate/" + resolution
    response = requests.get(url, headers=headers)
    if (response.status_code == 200):
        return jsonify({"msg": "Candidato eliminado con éxito"}), 200
    return response


# >>>> Users
@app.route("/users/", methods=["GET"])
def getUsers():
    url = url_security + "/users"
    response = requests.get(url, headers=headers)
    return Response(json.dumps(json.loads(response.content)),  mimetype='application/json')



@app.route("/users/<string:id>", methods=["GET"])
def getUser(id):
    url = url_security + "/users/" + id
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/users/<string:id>", methods=['PUT'])
def updateUser(id):
    url = url_security + "/users/" + id
    body = request.get_json()
    response = requests.put(url, json=body, headers=headers)
    return response.json()


@app.route("/users/", methods=["POST"])
def createUser():
    url = url_security + "/users"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/users/<string:id_user>/role/<string:id_role>", methods=["PUT"])
def assignRoleToUser(id_user, id_role):
    url = url_security + "/users/"+id_user + "/role/"+id_role
    response = requests.put(url, headers=headers)
    return response.json()


@app.route("/users/<string:id>", methods=["DELETE"])
def deleteUser(id):
    url = url_security + "/users/" + id
    response = requests.delete(url, headers=headers)
    if(response.status_code==204):
        return jsonify({"msg": "Usuario eliminado con éxito"}), 204
    return response


# >>>>>>> Roles
@app.route("/roles/", methods=["GET"])
def getRoles():
    url = url_security + "/roles"
    response = requests.get(url, headers=headers)
    return Response(json.dumps(json.loads(response.content)),  mimetype='application/json')


@app.route("/roles/", methods=["POST"])
def createRole():
    url = url_security + "/roles"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/roles/<string:id>", methods=["GET"])
def getRoleById(id):
    url = url_security + "/roles/" + id
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/roles/<string:id>", methods=['PUT'])
def updateRole(id):
    url = url_security + "/roles/" + id
    body = request.get_json()
    response = requests.put(url, json=body, headers=headers)
    return response.json()

@app.route("/roles/<string:id>", methods=["DELETE"])
def deleteRole(id):
    url = url_security + "/roles/" + id
    response = requests.delete(url, headers=headers)
    if(response.status_code==204):
        return jsonify({"msg": "Rol eliminado con éxito"}), 204
    return response

# >>>>>>>


'''Server Initialization'''
url = "http://" + dataConfig["url-apigateway"] + ":" + dataConfig["port-apigateway"]
print("Server running: " + url)
serve(app, host=dataConfig["url-apigateway"], port=dataConfig["port-apigateway"])

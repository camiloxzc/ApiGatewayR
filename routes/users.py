import requests
import json
from flask import request
from flask import Response
from main import headers, url_security, app
from flask import jsonify


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

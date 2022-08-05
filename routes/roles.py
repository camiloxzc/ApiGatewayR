import requests
import json
from flask import request
from flask import Response
from main import headers, url_security, app
from flask import jsonify


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


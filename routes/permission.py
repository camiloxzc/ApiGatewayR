import requests
import json
from flask import request
from flask import Response
from main import headers, url_security, app
from flask import jsonify


@app.route("/permissions/", methods=["GET"])
def getPermissions():
    url = url_security + "/permissions"
    response = requests.get(url, headers=headers)
    return Response(json.dumps(json.loads(response.content)),  mimetype='application/json')


@app.route("/permissions/", methods=["POST"])
def createPermission():
    url = url_security + "/permissions"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


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


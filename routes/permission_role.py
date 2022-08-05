import requests
import json
from flask import request
from flask import Response
from main import headers, url_security, app
from flask import jsonify


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



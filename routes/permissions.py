import requests
from flask import request
from main import headers, url_security, app

@app.route("/rolpermissions", methods=["GET"])
def getRolPermissions():
    url = url_security + "/rolpermissions"
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/rolpermission/<string:rol>", methods=["GET"])
def getRolPermission(rol):
    url = url_security + "/rolpermission/" + rol
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/rolpermission/<string:rol>", methods=['PUT'])
def updateRolPermission(rol):
    url = url_security + "/rolpermission/" + rol
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()

import requests
from flask import request
from main import headers, url_security, app


@app.route("/users/<string:id>", methods=["GET"])
def getUsers():
    url = url_security + "/users"
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/user/<string:id>", methods=["GET"])
def getUser(id):
    url = url_security + "/user/" + id
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/user", methods=["POST"])
def createUser():
    url = url_security + "/user"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/user/<string:id>", methods=['PUT'])
def updateUser(id):
    url = url_security + "/user/" + id
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/user/<string:id>", methods=["DELETE"])
def deleteUser(id):
    url = url_security + "/user/" + id
    response = requests.get(url, headers=headers)
    return response.json()

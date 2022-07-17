import requests
from flask import request
from main import headers, url_base, app


@app.route("/partys", methods=["GET"])
def getPartys():
    url = url_base + "/partys"
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/party/<string:id>", methods=["GET"])
def get_party(id):
    url = url_base + "/party/" + id
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/party", methods=["POST"])
def createParty():
    url = url_base + "/party"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()

@app.route("/party/<string:id>", methods=['PUT'])
def updateParty(id):
    url = url_base + "/party/" + id
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()

@app.route("/party/<string:id>", methods=["DELETE"])
def deleteParty(id):
    url = url_base + "/party/" + id
    response = requests.get(url, headers=headers)
    return response.json()

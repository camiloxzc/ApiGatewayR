import requests
from flask import request
from main import headers, url_base, app
from flask import Response
import json



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
import requests
from flask import request
from main import headers, url_base, app


@app.route("/candidates", methods=["GET"])
def getCandidates():    
    url = url_base + "/candidates"
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/candidate/<string:resolution>", methods=["GET"])
def getParty(resolution):
    url = url_base + "/candidate/" + resolution
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/candidate", methods=["POST"])
def createCandidate():
    url = url_base + "/candidate"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/candidate/<string:resolution>", methods=['PUT'])
def updateCandidate(resolution):
    url = url_base + "/candidate/" + resolution
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/candidate/<string:resolution>", methods=["DELETE"])
def deleteCandidate(resolution):
    url = url_base + "/candidate/" + resolution
    response = requests.get(url, headers=headers)
    return response.json()

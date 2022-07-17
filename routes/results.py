import requests
from main import headers, url_base, app

@app.route("/resultsbycandidate", methods=["GET"])
def getResultsByCandidate():    
    url = url_base + "/resultsbycandidate"
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/resultsbyparty", methods=["GET"])
def getResultsByParty():
    url = url_base + "/resultsbyparty"
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/resultsbytable", methods=["GET"])
def getResultsByTable():
    url = url_base + "/resultsbytable"
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/newsenate", methods=["GET"])
def getNewSenate():
    url = url_base + "/newsenate"
    response = requests.get(url, headers=headers)
    return response.json()


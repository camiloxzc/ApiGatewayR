import requests
from flask import request
from main import headers, url_base, app
from flask import Response
import json


@app.route("/tables/", methods=['GET'])
def get_tables():
    url = url_base + "/tables"
    response = requests.get(url, headers=headers)
    return Response(json.dumps(json.loads(response.content)),  mimetype='application/json')


@app.route("/table/", methods=['POST'])
def create_table():
    url = url_base + "/table"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=['GET'])
def get_table(id):
    url = url_base + "/table/" + id
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=['PUT'])
def update_table(id):
    url = url_base + "/table/" + id
    body = request.get_json()
    response = requests.put(url, json=body, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=["DELETE"])
def deleteTable(id):
    url = url_base + "/table/" + id
    response = requests.delete(url, headers=headers)
    return response.json()

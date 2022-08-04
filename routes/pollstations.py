import requests
import json
from flask import request, jsonify
from main import headers, url_base, app


@app.route("/tables", methods=['GET'])
def get_tables():
    url = url_base + "/tables"
    response = requests.get(url, headers=headers)
    re = json.loads(response.content)
    return jsonify(re), 200


@app.route("/table", methods=['POST'])
def create_table():
    url = url_base + "/table"
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=['GET'])
def get_table(id):
    url = url_base + "/tables/" + id
    response = requests.get(url, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=['PUT'])
def update_table(id):
    url = url_base + "/table/" + id
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()


@app.route("/table/<string:id>", methods=["DELETE"])
def deleteTable(id):
    url = url_base + "/table/" + id
    response = requests.get(url, headers=headers)
    return response.json()

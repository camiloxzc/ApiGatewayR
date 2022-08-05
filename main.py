from flask import Flask
from flask_cors import CORS
from flask import request
import requests
from flask_jwt_extended import verify_jwt_in_request,get_jwt_identity
from flask import jsonify
from waitress import serve
from flask_jwt_extended import JWTManager
import re

import middlewares.format_url



'''Setting Flask App'''
app = Flask(__name__)
cors = CORS(app)


'''Settings'''
from settings import dataConfig

app.config["JWT_SECRET_KEY"] = dataConfig["jwt-key"]
jwt = JWTManager(app)
url_base = dataConfig["url-administration"]
url_security = dataConfig["url-security"]


''' Middlewares '''


@app.before_request
def before_request_callback():
    print("before_request_callback started")
    excluded_routes = ["/auth"]
    if request.path not in excluded_routes:
        if not verify_jwt_in_request():
            return jsonify({"msg": "Permission denied"}), 401
        # Roles
        user = get_jwt_identity()
        print(user)
        if user["role"] is None:
            return jsonify({"msg": "Permission Denied"}), 401
        else:
            role_id = user["role"]["id"]
            route = format_url()
            method = request.method
            has_permission = validate_permission(role_id, route, method)
            if not has_permission:
                return jsonify({"msg": "Permission Denied"}), 401


def format_url():
    parts = request.path.split("/")
    url = request.path
    for part in parts:
        if re.search('\\d', part):
            url = url.replace(part, "?")
    return url


def validate_permission(role_id, route, method):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-security"] + "/permission-role/validate/role/" + role_id
    body = {"url": route, "metodo": method}
    print(body)
    response = requests.post(url, json=body, headers=headers)
    print(response)
    try:
        data = response.json()
        if "_id" in data:
            return True
    except:
        return False

'''Endpoint Routes'''
headers = {"Content-Type": "application/json; charset=utf-8"}
# >>>> Results 
import routes.results
# >>>> Poll Stations
import routes.pollstations
# >>>> Political Parties
import routes.parties
# >>>> Candidates
import routes.candidates
# >>>> Users
import routes.users
# >>>> Permissions
import routes.permission_role
# >>>> Token and Validation
import routes.validation


'''Server Initialization'''
url = "http://" + dataConfig["url-apigateway"] + ":" + dataConfig["port-apigateway"]
print("Server running: " + url)
serve(app, host=dataConfig["url-apigateway"], port=dataConfig["port-apigateway"])

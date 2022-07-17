from flask import Flask
from flask_cors import CORS
from waitress import serve
from flask_jwt_extended import JWTManager


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
import middlewares.before_request


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
import routes.permissions
# >>>> Token and Validation
import routes.validation


'''Server Initialization'''
url = "http://" + dataConfig["url-apigateway"] + ":" + dataConfig["port-apigateway"]
print("Server running: " + url)
serve(app, host=dataConfig["url-apigateway"], port=dataConfig["port-apigateway"])

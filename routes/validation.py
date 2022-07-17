import requests
import datetime
from flask import request, jsonify
from flask_jwt_extended import create_access_token

from main import headers, url_security, app


@app.route("/auth", methods=["POST"])
def login():
    # FE -> AGW
    data = request.get_json()
    # AGW -> MS
    url = url_security + "/users/validate"
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 401:
        return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401
    elif response.status_code == 500:
        return jsonify({"msg": "Error inesperado"}), 500
    elif response.status_code == 200:
        user = response.json()
        expires = datetime.timedelta(seconds=60 * 60 * 24)
        access_token = create_access_token(identity=user, expires_delta=expires)
        return jsonify({"token": access_token, "user_id": user["_id"]})

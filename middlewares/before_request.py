from main import app
from flask import request
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request,get_jwt_identity

from middlewares import format_url
from middlewares import validate_permission

@app.before_request
def before_request_callback():
    excluded_routes = ["/login"]
    if request.path not in excluded_routes:
        if not verify_jwt_in_request():
            return jsonify({"msg": "Permission denied"}), 401
        # Roles
        user = get_jwt_identity()
        print(user)
        if user["role"] is None:
            return jsonify({"msg": "Permission Denied"}), 401
        else:
            role_id = user["role"]["_id"]
            route = format_url()
            method = request.method
            has_permission = validate_permission(role_id, route, method)
            if not has_permission:
                return jsonify({"msg": "Permission Denied"}), 401

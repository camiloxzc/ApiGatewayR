from flask import request
from flask_jwt_extended import verify_jwt_in_request,get_jwt_identity
from flask import jsonify

from middlewares.format_url import *
from middlewares.validate_permission import *


def before_request_body(dataConfig):
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




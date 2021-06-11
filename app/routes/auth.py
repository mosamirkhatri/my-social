import os
from datetime import datetime, timedelta
from flask import Blueprint, request, make_response
from app.utils.helpers import login_schema, register_schema, validate_request, query_database, generate_token
from app.utils.decorators.login_required import login_required
from app.utils.helper_classes import AESCipher
from app.database.queries import Query

auth = Blueprint('auth', __name__)
cipher = AESCipher(os.environ.get('SECRET_KEY', "123456"))


@auth.route("/register", methods=['POST'])
def register():
    try:
        request_data = request.get_json()
        schema = register_schema()
        [valid, error] = validate_request(request_data, schema)
        if not valid:
            return {"success": False, "error": error}, 400
        first_name = request_data.get('first_name').strip()
        last_name = request_data.get('last_name').strip()
        username = request_data.get('username')
        password = request_data.get('password')

        user = query_database(Query.EXISTING_USER, (username))
        if(user):
            return {"success": False, "message": "User Already Exists"}, 409

        encrypted_password = cipher.encrypt(password)
        query_database(Query.CREATE_NEW_USER, (first_name,
                       last_name, username, encrypted_password))
        return {"success": True, "message": "User Successfully Created"}, 200
    except Exception as e:
        return {"success": False, "message": str(e.args)}, 500


@auth.route("/login", methods=['POST'])
def login():
    try:
        request_data = request.get_json()
        schema = login_schema()
        [valid, error] = validate_request(request_data, schema)
        if not valid:
            error_message = ", ".join(error.keys()) + " is/are invalid"
            return {"success": False, "error": error_message}, 400
        username = request_data.get('username')
        password = request_data.get('password')
        user = query_database(Query.EXISTING_USER, (username))
        if not user:
            return {"success": False, "message": "User Not Found"}, 404
        if password != cipher.decrypt(user.get('password')):
            return {"success": False, "message": "Invalid Credentials"}, 409
        payload = {"id": user.get("id"), "username": user.get("username"), "aud": "user",
                   "iat": int(datetime.utcnow().timestamp()), "exp": int((datetime.now() + timedelta(minutes=1)).timestamp())}
        token = generate_token(payload)
        resp = make_response({"data": {"id": user.get("id"), "username": user.get("username"),
                                       "first_name": user.get("first_name"), "last_name": user.get("last_name")},
                              "success": True}, 200)
        resp.set_cookie("token", token)
        return resp
    except Exception as e:
        return {"success": False, "message": str(e.args)}, 500


@auth.route("/logout", methods=['POST'])
@login_required
def logout():
    try:
        resp = make_response(
            {"success": True, "message": "Logged out successfully"}, 200)
        resp.delete_cookie('token')
        return resp
    except Exception as e:
        return {"success": False, "message": str(e.args)}, 500

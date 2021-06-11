from flask import request
from functools import wraps
import jwt
import os


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.cookies['token']
            parsed_token = jwt.decode(token, os.environ.get(
                'SECRET_KEY'), audience=["user"], algorithms="HS256")
            current_user = {"id": parsed_token["id"],
                            "username": parsed_token["username"]}
        except jwt.DecodeError:
            return {"success": False, "message": "Failed to decode token"}, 401
        except jwt.InvalidAudienceError:
            return {"success": False, "message": "Access denied"}, 403
        except jwt.ExpiredSignatureError:
            return {"success": False, "message": "Token Expired"}, 403
        except jwt.InvalidIssuedAtError:
            return {"success": False, "message": "Token can be used in future"}, 403
        except jwt.InvalidTokenError:
            return {"success": False, "message": "Invalid token"}, 401
        except Exception as e:
            return {"success": False, "message": "Token not provided or invalid"}, 400
        return f(current_user, *args, **kwargs)
    return decorated_function

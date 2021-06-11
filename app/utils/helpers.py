import pymysql.cursors
from pymysql import MySQLError
from cerberus import Validator
import jwt
import os
from app.config import Config


def query_database(query, parameter_values=None):
    connection = pymysql.connect(host=Config.MySql.DATABASE_SERVER, user=Config.MySql.DATABASE_USER,
                                 password=Config.MySql.DATABASE_PASS, db=Config.MySql.DATABASE_NAME,
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        cursor = connection.cursor()
        cursor.execute(query, parameter_values)
        result = []
        if cursor.rowcount == 1:
            result = cursor.fetchone()
        elif cursor.rowcount > 1:
            result = cursor.fetchall()
        return result
    except MySQLError as e:
        connection.rollback()
        # print("Error %d: %s" % (e.args[0], e.args[1]))
        raise e
    finally:
        connection.commit()
        connection.close()


def generate_token(payload):
    token = jwt.encode(payload, os.environ.get(
        'SECRET_KEY', "123456"), algorithm='HS256')
    return token


def validate_request(request_body, schema):
    v = Validator()
    valid = v.validate(request_body, schema)
    return valid, v.errors


def register_schema():
    """
    docstring
    """
    schema = {
        'first_name': {"type": "string", "minlength": 3, "maxlength": 50, "required": True, "regex": "^[A-Za-z ]+$"},
        'last_name': {"type": "string", "minlength": 3, "maxlength": 50, "required": True, "regex": "^[A-Za-z ]+$"},
        'username': {"type": "string", "minlength": 3, "maxlength": 50, "required": True, "regex": "^[A-Za-z]+$"},
        'password': {"type": "string", "minlength": 8, "maxlength": 50, "required": True, "regex": "^(?=.*\d)(?=.*[a-z]).{8,}$"},
    }
    return schema


def login_schema():
    """
    docstring
    """
    schema = {
        'username': {"type": "string", "minlength": 3, "maxlength": 50, "required": True, "regex": "^[A-Za-z]+$"},
        'password': {"type": "string", "minlength": 8, "maxlength": 50, "required": True, "regex": "^(?=.*\d)(?=.*[a-z]).{8,}$"},
    }
    return schema

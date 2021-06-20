
from functools import wraps
import re
from flask_restful import Resource, reqparse
from flask_restful import abort
from ..database import token_db
from flask import make_response, jsonify

token_parser = reqparse.RequestParser()
token_parser.add_argument(reqparse.Argument('token', required=True, type=str,
                                            help="The user's access token"))

_token_ctx = None


def get_token_ctx_data() -> dict:
    if _token_ctx != None:
        return _token_ctx

    raise Exception(
        "User tried to get token outside token required context, make sure you are using a 'requires_token' based decorator")


def requires_token(func):
    def wrapper(*args, **kwargs):
        global _token_ctx
        token_data = token_parser.parse_args(strict=True)
        dat = token_db.get_token_data(token_data['token'])
        if dat == None:
            ret = {'message': "This token does not exist or is expired"}
            return make_response(jsonify(ret), 400)
        _token_ctx = dat
        result = func(*args, **kwargs)
        _token_ctx = None
        return result
    return wrapper


@requires_token
def allowed_users(*roles):
    """Only users with the given roles will be able to access the function
    if the user is unathorized abort with 401
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token_data = token_parser.parse_args(strict=True)
            dat = token_db.get_token_data(token_data['token'])

            if dat['type'] not in roles:
                abort(401)
            result = func(*args, **kwargs)
            return result

        return wrapper
    return decorator

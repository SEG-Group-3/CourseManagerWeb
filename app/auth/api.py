from app.auth.api_helpers import get_token_ctx_data, requires_token
from flask_restful import Resource, reqparse
from ..plugins import api
from flask import make_response, jsonify
from ..database import users_db as u_manage
from ..database import token_db


login_parser = reqparse.RequestParser()


login_parser.add_argument(reqparse.Argument('userName', required=True, type=str,
                                            help="The user's username"))
login_parser.add_argument(reqparse.Argument('password', required=True, type=str,
                                            help="The user's password"))


token_parser = reqparse.RequestParser()
token_parser.add_argument(reqparse.Argument('token', required=True, type=str,
                                            help="The user's access token"))

register_parser = reqparse.RequestParser()
register_parser.add_argument(reqparse.Argument('userName', required=True, type=str,
                                               help="The user's username"))
register_parser.add_argument(reqparse.Argument('password', required=True, type=str,
                                               help="The user's password"))
register_parser.add_argument(reqparse.Argument('role', type=str,
                                               help="The user's role: Student or Instructor", default="Student"))


class LoginR(Resource):
    def post(self):
        # Authenticate
        login_data = login_parser.parse_args(strict=True)
        if(not u_manage.is_valid_cred(login_data['userName'], login_data['password'])):
            return make_response(jsonify({'message': "Bad credentials"}), 401)

        # Generate and return login token

        ret = {'message': "Token created",
               'token': token_db.create_token(login_data['userName'])}
        return make_response(jsonify(ret), 200)


class LogoutR(Resource):
    @requires_token
    def post(self):
        dat = get_token_ctx_data()
        token_db.delete_token(dat.get("token"))
        ret = {'message': "Goodbye"}
        return make_response(jsonify(ret), 404)


class RegisterR(Resource):
    def post(self):
        registration_data = register_parser.parse_args(strict=True)
        if not u_manage.add_user(registration_data):
            ret = {'message': "This username already exists!"}
            return make_response(jsonify(ret), 405)

        ret = {'message': "Account created"}
        return make_response(jsonify(ret), 200)


class WhoAmIR(Resource):
    @requires_token
    def get(self):
        dat = get_token_ctx_data()

        ret = {'message': "You are " + dat.get('userName')}
        return make_response(jsonify(ret), 200)


api.add_resource(LoginR, '/api/auth/login')
api.add_resource(LogoutR, '/api/auth/logout')
api.add_resource(RegisterR, '/api/auth/register')
api.add_resource(WhoAmIR, '/api/auth/whoami')

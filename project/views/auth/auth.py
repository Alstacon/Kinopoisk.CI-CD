from flask import request, abort
from flask_restx import Namespace, Resource

from project.container import auth_service
from project.setup.api.models import tokens_model
from project.setup.api.parsers import auth_parser

api = Namespace('auth')


@api.route('/login/')
class AuthView(Resource):

    @api.response(code=400, description='Bad request')
    @api.marshal_with(tokens_model, code=200, description='Tokens generated')
    def post(self):
        """Login user"""
        tokens = auth_service.generate_tokens(request.json)
        return tokens

    @api.response(code=401, description='Invalid refresh token')
    @api.marshal_with(tokens_model, code=200, description='Tokens updated')
    def put(self):
        data = request.json
        tokens = auth_service.approve_refresh_token(data.get('refresh_token'))
        return tokens


@api.route('/register/')
class AuthView(Resource):

    @api.expect(auth_parser)
    def post(self):
        """Create new user in db"""

        auth_service.create_user(auth_parser.parse_args())

        return '', 200

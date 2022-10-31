from flask import request
from flask_restx import Namespace, Resource

from project.models import User
from project.setup.api.models import user_model

from project.container import user_service
from project.tools.decorators import auth_required

api = Namespace('user')


@api.doc(security='Bearer')
@api.response(code=401, description='Unauthorized')
@api.response(code=404, description='Bad request')
@api.route('/', endpoint='profile_view')
class UserView(Resource):
    @api.marshal_with(user_model, code=200)
    @auth_required
    def get(self, user: User):
        user = user_service.get_item(user.email)
        return user

    @api.marshal_with(user_model, code=204)
    @auth_required
    def patch(self, user):
        data = request.json
        user_service.update(user, data)
        return ""


@api.doc(security='Bearer')
@api.route('/password/')
class UserPassChangeView(Resource):
    @api.marshal_with(user_model, code=200)
    @auth_required
    def put(self, user):
        data = request.json
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        user_service.update_password(user, old_password, new_password)
        return ""

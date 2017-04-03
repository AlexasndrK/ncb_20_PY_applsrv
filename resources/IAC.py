import db
from flask_restful import Resource, reqparse


class User(Resource):  # POST - also can be used for GET and UPDATE
    def get(self, user):
        pass

    def post(self):
        pass

    def delete(self, user):
        pass


class ResetUserPassword(Resource):  # POST
    def post(self):
        pass


class UserLogin(Resource):  # POST
    def post(self):
        pass


class GetUserConferences(Resource):
    def get(self, user):
        pass

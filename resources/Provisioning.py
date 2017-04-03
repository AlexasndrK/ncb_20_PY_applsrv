import db
from flask_restful import Resource, reqparse


class ProvisionConference(Resource):  # POST
    def post(self):
        pass

    def get(self, room):   # GET
        pass

    def delete(self, confid):
        pass


class UpdateProvisionConf(Resource):   # POST ?! - should be UPDATE or PUT
    def post(self):
        pass


class GetAllConferenceRooms(Resource):  # GET
    def get(self, custid):
        pass


class GetConferences(Resource):  # GET
    def get(self, vcb):
        pass

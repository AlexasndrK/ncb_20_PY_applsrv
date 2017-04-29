"""
 Project code: FCONF
 Development code: NCB-20
 File: PROVISIONING.PY
 File location: ../flask-dev/resources/
 type: Python 2.7
 Description: Program module containing API functions referred to as Provisioning and Reflection
 data in Web server features
"""
import db
from flask_restful import Resource, reqparse


class ProvisionConference(Resource):  # POST
    def post(self):
        pass

    def get(self, room):   # GET
        pass

    def delete(self, confid):
        pass


class UpdateProvisionConf(Resource):   # POST ?! - should be PUT
    def post(self):
        pass


class GetAllConferenceRooms(Resource):  # GET
    def get(self, custid):
        pass


class GetConferences(Resource):  # GET
    def get(self, vcb):
        pass

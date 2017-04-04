"""
 Project code: FCONF
 Development code: NCB-20
 File: RECORDING.PY
 File location: ../flask-dev/resources/
 type: Python 2.7
 Description: Program module containing API functions referred to as Conference and Greetings Recording
 data in Web server features
"""
import ESL
import db
from flask_restful import Resource


class Recording(Resource):  # GET
    def get(self, uuid):
        pass

    def delete(self, uuid):  # DELETE
        pass


class GetRecordings(Resource):  # GET
    def get(self, room):
        pass


class DoRecording(Resource):  # GET
    def get(self, room):
        pass


class GreetingRecord(Resource):  # GET
    def get(self, dnis):
        pass


class GreetingPlayback(Resource):  # GET
    def get(self, room):
        pass

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

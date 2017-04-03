"""
 Project code: FCONF
 Development code: NCB-20
 File: FREESWITCH.PY
 File location: ../flask-dev/resources/
 type: Python 2.7
 Description: Program module containing API functions referred to as Conference room moderation features
"""
from db import db
from flask_restful import Resource
import ESL


class UndeafConferenceRoom(Resource):
    def get(self, room):
        pass


class DeafConferenceRoom(Resource):
    def get(self, room):
        pass


class GetConferenceRoomInfo(Resource):
    def get(self, room):
        pass


class LockConferenceRoom(Resource):
    def get(self, room):
        pass


class UnlockConferenceRoom(Resource):
    def get(self, room):
        pass


class Dial(Resource):
    def get(self, dnis, ani):
        pass


class MuteConferenceRoom(Resource):
    def get(self, room):
        pass


class UnmuteConferenceRoom(Resource):
    def get(self, room):
        pass


class ToggleMuteConferenceUser(Resource):
    def get(self, room, uuid):
        pass


class DeafConferenceUser(Resource):
    def get(self, room, uuid):
        pass


class UndeafConferenceUser(Resource):
    def get(self, room, uuid):
        pass


class GetBridges(Resource):
    def get(self, custid):
        pass

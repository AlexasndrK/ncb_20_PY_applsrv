"""
 Project code: FCONF
 Development code: NCB-20
 File: IAC.PY
 File location: ../flask-dev/resources/
 type: Python 2.7
 Description: Program module containing API functions referred to as Identification & Access Control features
"""
import db
from flask_restful import Resource, reqparse
from flask import jsonify


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


class GetObjectConfig(Resource):
    def get(self, _type, _id):
        if _type == "organization":
            idType = 'orgid'
        elif _type == "partner":
            idType = 'partntid'
        else:
            return {"result": False, "reason": "Wrong method, There is no such type - {}".format(_type)}
        sql = "SELECT * FROM {} WHERE {} = {}".format(_type, idType, _id)
        cond = db.ncbDB()
        row = cond.ncb_getQuery(sql)
        if row:
            if len(row) == 1:
                return jsonify(row[0])
        return {"result": False}  # Maybe add reason

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


class User(Resource):  # POST - also can be used for GET and UPDATE
    def get(self, user):
        dbcon = db.ncbDB()
        sql = 'SELECT id FROM users WHERE user={}'.format(user)
        eslServer = dbcon.ncb_getQuery(sql)
        if len(eslServer) == 0 or len(eslServer) > 1:
            return{"result": False, "why": "I dont know.  I didnt code any debug here..."}
        else:
            id = eslServer["id"]
            return{"result": True, "id": id}

    def post(self):
        pass

    def delete(self, user):
        dbcon = db.ncbDB()
        sql1 = 'delete from users where user={}'.format(user)
        eslServDel = dbcon.ncb_pushQuery(sql1)
        if len(eslServDel) > 0:
            sql2 = 'select id from users where user={}'.format(user)
            eslServId = dbcon.ncb_getQuery(sql2)
            id = eslServId["id"]
            sql3 = 'delete from user2conf where userid=id'
            eslServDel = dbcon.ncb_pushQuery(sql3)
            return{"result": True}
        else:
            return{"result": False, "why": "Broke deleting user links"}


class ResetUserPassword(Resource):  # POST
    def post(self):
        pass


class UserLogin(Resource):  # POST
    def post(self):
        pass


class GetUserConferences(Resource):
    def get(self, user):
        pass

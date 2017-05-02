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
from flask import jsonify, request


class User(Resource):  # POST - also can be used for GET and UPDATE
    def get(self, user):
        dbcon = db.ncbDB()
        sql = "SELECT id FROM users WHERE user = '{}'".format(user)
        row = dbcon.ncb_getQuery(sql)
        if row is None or False:
            return{"result": False, "why": "Something happened"}
        else:
            uid = row[0]
            _id = uid['id']
            return{"result": True, "userid": _id}

    def post(self):
        pass

    def delete(self, user):
        pass


class ResetUserPassword(Resource):  # POST
    def post(self):
        pass


class UserLogin(Resource):  # POST
    def post(self):
        data = request.get_json()
        dbcon = db.ncbDB()
        sql = "SELECT pid FROM ideintity WHERE login = '{}' AND password = '{}'".format(data['user'], data['password'])
        row = dbcon.ncb_getQuery(sql)
        if row:
            tpid = row[0]
            if len(tpid) != 0:
                pid = tpid['pid']
                sql = "SELECT role FROM rbac WHERE pid = '{}'".format(pid)
                rrow = dbcon.ncb_getQuery(sql)
                if rrow:
                    trole = rrow[0]
                    role = trole['role']
                    return {"result": True, "pid": pid, "role": role}
        return {"result": False, "reason": "Nothing was found..."}


class GetUserConferences(Resource):
    def post(self, user):
        dbcon = db.ncbDB()
        sql = "select conf from user2conf where userid={}".format(user)
        row = dbcon.ncb_getQuery(sql)

        if len(row) == 0:
            return{"result": False, "why": "need to assign some rooms to this guy..."}
        else:
            return{"result": True, "conf_rooms": row}


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


class GetACobjectStart(Resource):
    def get(self, pid, role):
        if role == admin:
            ind = 'oranization_orgid'
        elif role == parner:
            ind = 'prtnid'
        else:
            return {"result": False, "why": "Wrond role"}
        condb = db.ncbDB()
        sql = "SELECT entrance FROM startentrance WHERE role = '{}'".format(role)
        table = condb.ncb_getQuery(sql)
        if table is None or False:
            return {"result": False, "why": "Can't find table according to role"}
        sql = "SELECT {} FROM {} WHERE rbac_pid = '{}'".format(ind, table, pid)
        row = conddb.ncb_getQuery(sql)
        if row:
            result = row[0]
            return {"result": True, "obj": result}
        else:
            return {"result": False, "why": "Can't find this user"}

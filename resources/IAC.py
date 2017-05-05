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


class GetObjRCprofile(Resource):
    def get(self, _type):
        if _type == "partner":
            tableid = "prtntid"
            profid = "prtnprofile_id"
            table = "prtnprofile"
        elif _type == "organization":
            tableid = "orgid"
            profid = "orgprofile_id"
            table = "orgprofile"
        else:
            return {"result": False, "why": "Wrong type, please check it - {}".format(_type)}
        sql = "SELECT {}.* FROM {}, {} WHERE {}.{} = '{}' AND  {}.profile_id = {}.{}".format(table, table, _type, _type, tableid, objid, table, _type, profid)
        print sql
        condb = db.ncbDB()
        profAtibutes = condb.ncb_getQuery(sql)
        if profAtibutes:
            if len(profAtibutes) == 1:
                return {"result": True, "body": profAtibutes[0]}
        return {"result": False, "why": "Can't fetch data or get more than one"}


class GetObjAdminList(Resource):
    def get(self, _type, objid):
        if _type == "partner":
            tableid = "prtnid"
            table = "admin2prtn"
        elif _type == "organization":
            tableid = "orgid"
            table = "admin2org"
        else:
            return {"result": False, "why": "Wrong type, please check it - {}".format(_type)}
        sql = "SELECT rbac_pid FROM {} WHERE {} = '{}'".format(table, tableid, objid)
        condb = db.ncbDB()
        adminList = condb.ncb_getQuery(sql)
        if adminList:
            adminListrow = [str(item['rbac_pid']) for item in adminList]
            adminListval = ','.join(elem for elem in adminListrow)
            sql = "SELECT first_name, last_name, email FROM ideintity WHERE pid in ({})".format(adminListval)
            adminAtribute = condb.ncb_getQuery(sql)
            if adminAtribute:
                return {"result": True, "body": adminAtribute}
        return {"result": False, "why": "Can't get data from DB"}


class GetVCBlist(Resource):
    def get(self, orgid):
        sql = "SELECT vcb_id, domain, language FROM vcb WHERE orgid = {}".format(orgid)
        condb = db.ncbDB()
        vcbList = condb.ncb_getQuery(sql)
        if vcbList:
            return {"result": True, "body": vcbList}
        return {"result": False, "why": "Can't retrive data from DB wih such ID - {}".format(orgid)}

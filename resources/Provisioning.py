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
        resConf = {}
        dbcon = db.ncbDB()
        sql = 'SELECT * FROM conf_room WHERE room_id={}'.format(room)
        eslServer = dbcon.ncb_getQuery(sql)
        if len(eslServer) > 0:
            sql1 = 'SELECT rid, vcb_id, room_id, attendee_pin, moderator_pin, spinuser, spinmod, maxallowed, type  FROM conf_room WHERE room_id={}'.format(room)
            row = dbcon.ncb_getQuery(sql1)
        else:
            sql1 = 'SELECT \"null\" AS vcb_id, rid,  room_id, attendee_pin, moderator_pin, spinuser, spinmod, maxallowed, type FROM conf_room WHERE room_id={}'.format(room)
            row = dbcon.ncb_getQuery(sql1)
        if len(row) == 0:
            return{"result": False, "why": "Can't fetch data from DB"}
        else:
            GetConf = row[0]
            GetConf["dnis"] = GetConf.pop("vcb_id")
            GetConf["confroom"] = GetConf.pop("room_id")
            GetConf["confpass"] = GetConf.pop("attendee_pin")
            GetConf["confadminpin"] = GetConf.pop("moderator_pin")
            GetConf["maxuser"] = GetConf.pop("maxallowed")
            GetConf["spinuser"] = GetConf.pop("spinuser")
            GetConf["spinmod"] = GetConf.pop("spinmod")
            GetConf["rid"] = GetConf.pop("rid")
            GetConf["parent"] = [""]
            rid = GetConf["rid"]

            if GetConf["type"] == ["scheduled"]:
                sql2 = 'SELECT duration, unix_timestamp(start_date) AS start_date FROM type_scheduled WHERE rid={}'.format(rid)
                rest = dbcon.ncb_getQuery(sql2)
                trow = rest[0]
                duratn = trow["duration"]
                sdate = trow["start_date"]
                time = sdate + duratn * 60
                GetConf["confexpired"] = time

            elif GetConf["type"] == ["recurring"]:
                sql2 = 'SELECT unix_timestamp(end_date) AS end_date FROM type_recurring WHERE rid={}'.format(rid)
                rest = dbcon.ncb_getQuery(sql2)
                trow = rest[0]
                edate = trow["end_date"]
                GetConf["confexpired"] = edate
            else:
                GetConf["confexpired"] = "-1"

        return GetConf

        def delete(self, confid):
            pass


class UpdateProvisionConf(Resource):   # POST ?! - should be PUT
    def post(self):
        pass


class GetAllConferenceRooms(Resource):  # GET
    def get(self, custid):
        pass


class GetConfroombyVCB(Resource):  # GET
    def get(self, vcb):
        if len(vcb) == 10 and vcb.isdigit():
            sql = "SELECT room_id from conf_room WHERE vcb_id = '{}'".format(vcb)
            condb = db.ncbDB()
            row = condb.ncb_getQuery(sql)
            if row:
                #  rowList = [n["room_id"] for n in row]
                vcbList = {vcb: row}
                return {"result": True, "body": vcbList}
        return {"result": False, "why": "Wrong phone number format or conf rooms not assigned"}

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
        sql = 'select * from conf_room where room_id={}'.format(room)
        eslServer = dbcon.ncb_getQuery(sql)
        if len(eslServer) > 0:
            sql1 = 'select rid, vcb_id, room_id, attendee_pin, moderator_pin, spinuser, spinmod, maxallowed, type  from conf_room where room_id={}'.format(room)
            row = dbcon.ncb_getQuery(sql1)
        else:
            sql1 = 'select \"null\" as vcb_id, rid,  room_id, attendee_pin, moderator_pin, spinuser, spinmod, maxallowed, type from conf_room where room_id={}'.format(room)
            row = dbcon.ncb_getQuery(sql1)
        if len(row) == 0:
            return{"result": False}
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
                sql2 = 'select duration, unix_timestamp(start_date) as start_date from type_scheduled where rid={}'.format(rid)
                rest = dbcon.ncb_getQuery(sql2)
                trow = rest[0]
                duratn = trow["duration"]
                sdate = trow["start_date"]
                time = sdate + duratn * 60
                GetConf["confexpired"] = time

            elif GetConf["type"] == ["recurring"]:
                sql2 = 'select unix_timestamp(end_date) as end_date from type_recurring where rid={}'.format(rid)
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


class GetConferences(Resource):  # GET
    def get(self, vcb):
        pass

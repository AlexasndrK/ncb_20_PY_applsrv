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
from flask import jsonify, request


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


class ObjectRP(Resource):
    def post(self):
        data = request.get_json()
        if data:
            if data["type"] == "partner":
                sql = "INSERT INTO prtnprofile  (maxports, maxduration, maxrecord, maxendless) VALUES ({},{},{},{})".format(data["maxports"], data["maxduration"], data["maxrecord"], data["maxendless"])
            elif data["type"] == "organization":
                sql = "INSERT INTO orgprofile  (maxports, maxduration, maxrecord, maxendless) VALUES ({},{},{},{})".format(data["maxports"], data["maxduration"], data["maxrecord"], data["maxendless"])
            elif data["type"] = "moderator":
                sql = "INSERT INTO moderRP  (maxports, maxduration, maxrecord, maxendless) VALUES ({},{},{},{})".format(data["maxports"], data["maxduration"], data["maxrecord"], data["maxendless"])
            condb = db.ncbDB()
            res = condb.ncb_pushQuery(sql)
            if res:
                return {"result": True, "body": "Profile information has been inserted"}
        return {"result": False, "why": "Wrong data or issue with DB"}

    def put(self):
        data = request.get_json()
        _type = data["type"]
        data.pop("type", None)
        if data:
            if _type = "patner":
                table = "prtnprofile"
            elif _type = "organization":
                table = "orgprofile"
            elif _type = "moderator":
                table = "moderPr"
            condb = db.ncbDB()
            for key in data:
                sql = "UPDATE prtnprofile SET {}={} where pid = {}".format(key, data[key], data["pid"])
                res = condb.ncb_pushQuery(sql)
                if res:
                    return {"result": True, "body": "Updated Successfully"}
        return {"result": False, "why": "Empty values or something wrong with DB"}

    def delete(self, pid, _type):
        if pid and _type:
            if _type == "partner":
                sql = "DELETE FROM prtnprofile  WHERE profile_id = '{}'".format(pid)
            elif _type == "organization":
                sql = "DELETE FROM orgprofile  WHERE profile_id = '{}'".format(pid)
            elif _type = "moderator":
                sql = "DELETE FROM moderRP  WHERE modRP_id = '{}'".format(pid)
            condb = db.ncbDB()
            res = condb.ncb_pushQuery(sql)
            if res:
                return {"result": True, "body": "Profile information has been deleted"}
        return {"result": False, "why": "Wrong data or issue with DB"}


class ModerAttributes(Resource):
    def post(self):
        data = request.get_json()
        if data:
            for key in data:
                if data["key"] is None:
                    return {"result": False, "why": "There is empty value for {}".formta(key)}
            condb = db.ncbDB()
            sql = "INSERT into moder_profile (pid, modPR_id, vcb_id) VALUES ({}, {}, {})".format(data["pid"], data["modPR_id"], data["vcb_id"])
            res = condb.ncb_pushQuery(sql)
            if res:
                return {"result": True, "body": "Successfully inserted "}
        return {"result": False, "why": "Something wrong with DB"}

    def put(self):
        data = request.get_json()
        if data:
            condb = db.ncbDB()
            for key in data:
                sql = "UPDATE moder_profile SET {}={} where pid = {}".format(key, data[key], data["pid"])
                res = condb.ncb_pushQuery(sql)
                if res:
                    return {"result": True, "body": "Updated Successfully"}
        return {"result": False, "why": "Empty values or something wrong with DB"}

    def delete(self, pid):
        if pid:
            condb = db.ncbDB()
            sql = "DELETE FROM moder_profile WHERE pid = '{}'".format(pid)
            res = condb.ncb_pushQuery(sql)
            if res:
                return {"result": True, "body": "Moderetor has beed deleted"}
        return {"result": False, "why": "Wrong data or missed value"}


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


class ConfRoomAttributes(Resource):
    def get(self, vcb_id, room_id):
        atribList = {"conf_room": '',
                     "attendees_invited": '',
                     "room_profile": '',
                     "type_attributes": ''}
        condb = db.ncbDB()
        sql = """SELECT vcb_id,
                        room_id,
                        attendee_pin,
                        moderator_pin,
                        maxallowed,
                        type,
                        spinuser,
                        spinmod
                 FROM conf_room
                 WHERE room_id = '{}'""".format(room_id)
        conf_room = condb.ncb_getQuery(sql)
        if conf_room:
            if len(conf_room) == 1:
                atribList["conf_room"] = conf_room[0]
        else:
            atribList["conf_room"] = False
        sql = """SELECT email,
                        contact_phone_number,
                        name
                 FROM attendees_invited
                 WHERE room_id = '{}'""".format(room_id)
        attendes = condb.ncb_getQuery(sql)
        if attendes:
            atribList["attendees_invited"] = attendes
        else:
            atribList["attendees_invited"] = False
        sql = """SELECT a.wait_for_moderator,
                        a.end_moder_leave,
                        a.join_sound,
                        a.lecture_mode,
                        a.record_name_path,
                        a.basic_profile,
                        a.energy_detection,
                        a.comfort_noise
                 FROM conference_room_profile as a
                 LEFT JOIN conf_room as b
                 ON b.profile_id = a.profile_id
                 WHERE b.room_id = '{}'""".format(room_id)
        room_profile = condb.ncb_getQuery(sql)
        print room_profile
        if room_profile:
            if len(room_profile) == 1:
                atribList["room_profile"] = room_profile[0]
        else:
            atribList["room_profile"] = False

        sql = """SELECT a.*
                 FROM type_{} as a, conf_room as b
                 WHERE b.room_id = '{}' AND a.rid = b.rid""".format(conf_room[0]["type"], room_id)

        type_attributes = condb.ncb_getQuery(sql)
        print type_attributes is not None
        if type_attributes:
            print len(type_attributes)
            if len(type_attributes) == 1:
                atribList["type_attributes"] = type_attributes[0]
        else:
            atribList["type_attributes"] = False
        for v in atribList.values():
            if v is False:
                return {"result": False, "why": "We can't get some elements"}
        print atribList
        return jsonify({"result": True, "body": atribList})

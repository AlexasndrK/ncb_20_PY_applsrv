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
import random


class Object(Resource):
    def post(self):
        data = request.get_json()
        if data:
            if data["type"] == "partner":
                sql = "INSERT INTO partner (company_name, domain, language, address, city, country, email, cphone, active, prtnprofile_id) VALUES ('{company_name}', '{domain}', '{language}', '{address}', '{city}', '{country}', '{email}', {cphone}, {active}, {prtnprofile_id})".format(**data)
            elif data["type"] == "organization":
                sql = "INSERT INTO organization (prtnid, organization_name, orgprofile_id) VALUES ('{}', '{}', '{}')".format(data["prtnid"], data["organization_name"], data["orgprofile_id"])
            else:
                return {"result": False, "why": "Wrong type of new object"}
            condb = db.ncbDB()
            res = condb.ncb_pushQuery(sql)
            if res:
                return {"result": True, "body": "New object has been added"}
        return {"result": False, "why": "Check DB or get request"}

    def put(self):
        data = request.get_json()
        if data:
            if data["type"] == "partner":
                table = "partner"
                pid = "prtnid"
            elif data["type"] == "organization":
                table = "organization"
                pid = "orgid"
            else:
                return {"result": False, "why": "Wrong type of updating object"}
            sql = "UPDATE {} SET company_name='{}', domain='{}', language='{}', address='{}', city='{}', country='{}',   email='{}', cphone='{}', active='{}', prtnprofile_id='{}' WHERE {} = '{}'".format(table, data["company_name"], data["domain"], data["language"], data["address"], data["city"], data["country"], data["email"], data["cphone"], data["active"], data["prtnprofile_id"], pid, data["pid"])
            condb = db.ncbDB()
            res = condb.ncb_pushQuery(sql)
            if res is False:
                    return {"result": False, "why": "something wtong with inserting in DB"}
            return {"result": True, "body": "Updated Successfull"}
        return {"result": False, "why": "Empty values or something wrong with DB"}

    def delete(self, pid):
        data = request.get_json()
        if pid:
            if data["type"] == "partner":
                sql = "DELETE FROM  partner WHERE prtnid = '{}'".format(pid)
            elif data["type"] == "organization":
                sql = "DELETE FROM  organization WHERE orgid = '{}'".format(pid)
            else:
                return {"result": False, "why": "Wrong type of new object"}
            condb = db.ncbDB()
            res = condb.ncb_pushQuery(sql)
            if res:
                return {"result": True, "body": "Object has been deleted"}
        return {"result": False, "why": "Check DB or get request"}


class ObjectRP(Resource):
    def post(self):
        data = request.get_json()
        if data:
            if data["type"] == "partner":
                sql = "INSERT INTO prtnprofile (maxports, maxduration, maxrecord, maxendless) VALUES ({}, {}, {}, {})".format(data["maxports"], data["maxduration"], data["maxrecord"], data["maxendless"])
            elif data["type"] == "organization":
                sql = "INSERT INTO orgprofile (maxports, maxduration, maxrecord, maxendless) VALUES ({}, {}, {}, {})".format(data["maxports"], data["maxduration"], data["maxrecord"], data["maxendless"])
            elif data["type"] == "moderator":
                sql = "INSERT INTO moderRP (maxports, maxduration, maxrecord, maxendless) VALUES ({},{},{},{})".format(data["maxports"], data["maxduration"], data["maxrecord"], data["maxendless"])
            condb = db.ncbDB()
            res = condb.ncb_pushQuery(sql)
            if res:
                return {"result": True, "body": "Profile information has been inserted"}
        return {"result": False, "why": "Wrong data or issue with DB"}

    def put(self):
        data = request.get_json()
        if data:
            if data["type"] == "patner":
                table = "prtnprofile"
                pid = "profile_id"
            elif data["type"] == "organization":
                table = "orgprofile"
                pid = "profile_id"
            elif data["type"] == "moderator":
                table = "moderRP"
                pid = "modRP_id"
            sql = "UPDATE {} SET maxports='{}', maxduration='{}', maxrecord='{}', maxendless='{}' WHERE {} = '{}' ".format(table, data["maxports"], data["maxduration"], data["maxrecord"], data["maxendless"], pid, data["pid"])
            condb = db.ncbDB()
            res = condb.ncb_pushQuery(sql)
            if res is False:
                return {"result": False, "why": "something wtong with inserting in DB"}
            return {"result": True, "body": "Updated Successfull"}
        return {"result": False, "why": "Empty values or something wrong with DB"}

    def delete(self, pid):
        data = request.get_json()
        if pid:
            if data["type"] == "partner":
                sql = "DELETE FROM prtnprofile  WHERE profile_id = '{}'".format(pid)
            elif data["type"] == "organization":
                sql = "DELETE FROM orgprofile  WHERE profile_id = '{}'".format(pid)
            elif data["type"] == "moderator":
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
            sql = "INSERT INTO moder_profile (pid, modRP_id, vcb_id) VALUES ({}, {}, {})".format(data["pid"], data["modRp_id"], data["vcb_id"])
            condb = db.ncbDB()
            res = condb.ncb_pushQuery(sql)
            if res:
                return {"result": True, "body": "Successfully inserted "}
        return {"result": False, "why": "Something wrong with DB"}

    def put(self):
        data = request.get_json()
        if data:
            sql = "UPDATE moder_profile SET  modRP_id='{}', vcb_id='{}' WHERE pid = '{}'".format(data["modRP_id"], data["vcb_id"], data["pid"])
            condb = db.ncbDB()
            res = condb.ncb_pushQuery(sql)
            if res:
                return {"result": True, "body": "Updated Successfully"}
        return {"result": False, "why": "Empty values or something wrong with DB"}

    def delete(self, pid):
        if pid:
            sql = "DELETE FROM moder_profile WHERE pid = '{}'".format(pid)
            condb = db.ncbDB()
            res = condb.ncb_pushQuery(sql)
            if res:
                return {"result": True, "body": "Moderetor has beed deleted"}
        return {"result": False, "why": "Wrong data or missed value"}


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
        return jsonify({"result": True, "body": atribList})

    class ConfRoom(Resource):
        def post(self):
            data = request.get_json()
            typeAtrrib = data["type"]
            if data:
                room_id, attendee_pin, moderator_pin = random.sample(xrange(100000, 999999), 3)
                spinuser, spinmod = random.sample(xrange(1000000, 9999999), 2)

                sql = "INSERT INTO conf_room (vcb_id, room_id, attendee_pin, moderator_pin, profile_id, maxallowed, type, spinuser, spinmod) VALUES ({}, {}, {}, {}, {}, {}, {}, {})".format(data["vcb_id"], room_id, attendee_pin, moderator_pin, data["maxallowed"], typeAtrrib["type"], spinuser, spinmod)

                condb = db.ncbDB()
                if condb:
                    res = condb.ncb_pushQuery(sql)
                    if res == "Duplicate error":
                        return {"result": False, "why": "This entry is already in DB. Try again"}
                    # INSERTING INTO TYPES TABLES
                    if typeAtrrib["type"] == "type_persistent":

                        sql = "INSERT INTO type_persistent (rid, TMZ, start_date, end_date) VALUES ('SELECT rid FROM conf_room WHERE vcb_id = {} AND room_id = {}', {}, {}, {})".format(data["vcb_id"], room_id, typeAtrrib["TMZ"], typeAtrrib["start_date"], typeAtrrib["end_date"])

                    if typeAtrrib["type"] == "type_scheduled":

                        sql = "INSERT INTO type_scheduled (rid, TMZ, can_be_prolonged, duration, start_date) VALUES ('SELECT rid FROM conf_room WHERE vcb_id = {} AND room_id = {}', {}, {}, {}, {})".format(data["vcb_id"], room_id, typeAtrrib["TMZ"], typeAtrrib["can_be_prolonged"], typeAtrrib["duration"], typeAtrrib["start_date"])

                    if typeAtrrib["type"] == "type_recurring":

                        sql = "INSERT INTO type_recurring (rid, TMZ, can_be_prolonged, recur, day_week, rec_interval, start_date, end_date, duration, count) VALUES ('SELECT rid FROM conf_room WHERE vcb_id = {} AND room_id = {}', {}, {}, {}, {}, {}, {}, {}, {}, {})".format(data["vcb_id"], room_id, typeAtrrib["TMZ"], typeAtrrib["can_be_prolonged"], typeAtrrib["recur"], typeAtrrib["day_week"], typeAtrrib["rec_interval"], typeAtrrib["start_date"], typeAtrrib["end_date"], typeAtrrib["duration"], typeAtrrib["count"])

                    res = condb.ncb_pushQuery(sql)
                    # INSERTING INTO conference_room_profile
                    if not res:
                        return {"result": False, "why": "Error inserting type Attributes"}

                    sql = "INSERT INTO conference_room_profile (rid, wait_for_moderator, end_moder_leave, join_sound, lecture_mode, basic_profile, energy_detection, comfort_noise) VALUES ('SELECT rid FROM conf_room WHERE vcb_id = {} AND room_id = {}', {}, {}, {}, {}, {}, {}, {})".format(data["vcb_id"], room_id, data["wait_for_moderator"], data["end_moder_leave"], data["join_sound"], data["lecture_mode"], data["basic_profile"], data["energy_detection"], data["comfort_noise"])

                    res = condb.ncb_pushQuery(sql)
                    if not res:
                        return {"result": False, "why": "Error inserting room attributes"}
                    return {"result": True, "body": {"vcb_id": data["vcb_id"], "room_id": room_id}}

        def put(self):
            data = request.get_json()
            if data:
                sql = "SELECT rid, type FROM conf_room WHERE room_id = '{}' AND vcb_id = '{}'".format(data["room_id"], data["vcb_id"])
                condb = db.ncbDB()
                typeAtrrib = data["type"]
                out = condb.ncb_getQuery(sql)
                if out:
                    rid = out[0]["rid"]
                    table = "type_" + out[0]["type"]
                    sql = "UPDATE conf_room SET attendee_pin = '{}', moderator_pin = '{}', maxallowed = '{}', spinuser = '{}', spinmod = '{}' WHERE rid = '{}'".format(data["attendee_pin"], data["moderator_pin"], data["maxallowed"], data["spinuser"], data["spinmod"], rid)
                    res = condb.ncb_pushQuery(sql)
                    if not res:
                        return = {"result": False, "why": "Can't Update data in  table - conf_room"}
                    if table == "type_persistent":
                        sql = "UPDATE {} SET TMZ = '{}', start_date = '{}', end_date = '{}' WHERE rid = '{}'".format(table, typeAtrrib["TMZ"], typeAtrrib["start_date"], typeAtrrib["end_date"])
                    elif table == "type_scheduled":
                        sql = "UPDATE {} SET TMZ = '{}', can_be_prolonged = '{}', duration = '{}', start_date = '{}' WHERE rid = '{}'".format(table, typeAtrrib["TMZ"], typeAtrrib["can_be_prolonged"], typeAtrrib["duration"], typeAtrrib["end_date"])
                    elif table == "type_recurring":
                        sql = "UPDATE {} SET TMZ = '{}', can_be_prolonged = '{}', recur = '{}', day_week = '{}', rec_interval = '{}', start_date = '{}', end_date = '{}', duration = '{}', count = '{}' WHERE rid = '{}'".format(table, typeAtrrib["TMZ"], typeAtrrib["can_be_prolonged"], typeAtrrib["recur"], typeAtrrib["day_week"], typeAtrrib["rec_interval"], typeAtrrib["start_date"], typeAtrrib["end_date"], typeAtrrib["duration"], typeAtrrib["count"])
                    else:
                        return {"result": False, "why": "Wrong conference room type"}
                    res = condb.ncb_pushQuery(sql)
                    if not res:
                        return {"result": False, "why": "Can't update data in table - {}".format(table)}
                    sql = "UPDATE conference_room_profile SET wait_for_moderator = '{}', end_moder_leave = '{}', join_sound = '{}', lecture_mode = '{}', basic_profile = '{}', energy_detection = '{}', comfort_noise = '{}' WHERE rid = '{}'".format(data["wait_for_moderator"], data["end_moder_leave"], data["join_sound"], data["lecture_mode"], data["basic_profile"], data["energy_detection"], data["comfort_noise"], rid)
                    res = condb.ncb_pushQuery(sql)
                    if not res:
                        return {"result": False, "why": "Can't update data in table - conference_room_profile"}
                    return {"result": True, "body": "Conference room - {} information has been updated".format(data["room_id"])}
            return {"result": False, "why": "Wrong data"}

        def delete(self, rid):
            data = request.get_json()
            if data:
                sql = "SELECT rid, type FROM conf_room WHERE room_id = '{}' AND vcb_id = '{}'".format(data["room_id"], data["vcb_id"])
                condb = db.ncbDB()
                out = condb.ncb_getQuery(sql)
                if out:
                    rid = out[0]["rid"]
                    table = out[0]["type"]

                    sql = "DELETE FROM conf_room INNER JOIN conference_room_profile ON conf_room.rid = conference_room_profile.rid INNER JOIN type_{0} ON conf_room.rid  = type_{0}.rid WHERE conf_room.rid = {1}".format(table, rid)

                    res = condb.ncb_pushQuery(sql)
                    if not res:
                        return {"result": False, "why": "Can't delete conference room {}. Check if exist".format(data["room_id"])}
                    return {"result": True, "body": "Conference room - {} - has been deleted from system".format(data["room_id"])}
                return {"result": False, "why": "There is no such conference room in the system"}
            return {"result": False, "why": "Can't get data from http message"}

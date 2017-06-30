"""
 Project code: FCONF
 Development code: NCB-20
 File: RECORDING.PY
 File location: ../flask-dev/resources/
 type: Python 2.7
 Description: Program module containing API functions referred to as Conference and Greetings Recording
 data in Web server features
"""
# TODO: Add fucntiom for deleting greeting file. Maybe DELETE method
import ESL
import db
import os
import re
from datetime import datetime
from flask_restful import Resource
from models.eslConf import *
from flask import send_from_directory, jsonify


media_path = "/media/conference"


# Maybe add check if no file
class Recording(Resource):
    def get(self, uuid):
        condb = db.ncbDB()
        sql = "SELECT file_path FROM conf_record WHERE uuid = {}".format(uuid)
        row = cond.ncb_getQuery(sql)
        if row:
            if len(row) == 1:
                rec = row[0]
                file_path, file_name = os.path.split(rec["file_path"])
                if os.path.isfile(rec["file_path"]):
                    content = send_from_directory(file_path, file_name, mimetype='audio/wav')
                    return {"resut": True, "filedata": {"filename": file_name, "data": content}}
        return {"result": False, "why": "Can't get data from DB"}

    def delete(self, uuid):  # DELETE
        pass


class GetRecordings(Resource):  # GET
    def get(self, room):
        cdb = db.ncbDB()
        sql = "SELECT t1.room_id AS confroom, t1.id as uuid, t1.record_time, t1.file_path AS filelocation FROM conf_record t1 JOIN conf_room t2 ON t1.room_id = t2.rid  WHERE t2.room_id = '{}'".format(room)
        row = cdb.ncb_getQuery(sql)
        if row:
            return jsonify(result=True, body=row)
        else:
            return {"result": False, "why": "Can't get list of records", "sql": sql}


# TODO: Add check for row variable if it's not False
class DoRecording(Resource):  # GET
    def get(self, method, room):
        conf = getConferenceIP(room)
        cdb = db.ncbDB()
        sql = "SELECT vcb_id, rid FROM conf_room WHERE room_id = {}".format(room)
        row = cdb.ncb_getQuery(sql)
        vcb = row[0]

        uuid = getConfUUID(room)
        method = str(method)
        timestamp = datetime.now()
        time = timestamp.strftime("%Y-%m-%d_%H-%M")
        rec_path = "{}/{}/records".format(media_path, vcb['vcb_id'])
        recfile = "{}/{}_rec_{}.wav".format(rec_path, room, time)
        con = ESL.ESLconnection(conf['ip'], '8021', 'ClueCon')
        if con.connected:
            if method.upper() == 'START':
                pattern = "recording_node"
                if re.search(pattern, str(conf['body'])) is None:
                    exe = con.api("conference conf_{} recording start {}".format(room, recfile))
                    sql = "INSERT INTO conf_record(room_id, file_path, uuid, record_time) VALUES ('{}', '{}', '{}', '{}')".format(vcb['rid'], recfile, uuid, timestamp)
                    cdb.ncb_pushQuery(sql)
                    out = exe.getBody().rstrip('\n')
                    return {"result": True, "why": "Started {}".format(out)}
                return {"result": False, "why": "Recording already started..."}
            elif method.upper() == 'STOP':
                sql = "SELECT id, file_path FROM conf_record WHERE uuid = '{}'".format(uuid)
                row = cdb.ncb_getQuery(sql)
                if row:
                    rec = row[0]
                    sql = "UPDATE conf_record SET uuid=NULL WHERE id = {}".format(rec['id'])
                    cdb.ncb_pushQuery(sql)
                    exe = con.api("conference conf_{} recording stop '{}'".format(room, rec['file_path']))
                    out = exe.getBody().rstrip("\n")
                    return {"result": True, "why": " {}".format(out)}
                else:
                    exe = con.api("conference conf_{} recording stop".format(room))
                    return {"result": False, "why": "We cant retrive uuid but we tried to stop record"}
            elif method.upper() == 'PAUSE':
                sql = "SELECT id, file_path FROM conf_record  WHERE uuid = '{}'".format(uuid)
                row = cdb.ncb_getQuery(sql)
                rec = row[0]
                if rec:
                    exe = con.api("conference conf_{} recording pause {}".format(room, rec['file_path']))
                    out = exe.getBody().rstrip("\n")
                    return {"result": True, "why": out}
            else:
                sql = "SELECT id, file_path FROM conf_record  WHERE uuid = '{}'".format(uuid)
                row = cdb.ncb_getQuery(sql)
                rec = row[0]
                if rec:
                    exe = con.api("conference conf_{} recording {} {}".format(room, method, rec['file_path']))
                    out = exe.getBody().rstrip("\n")
                    return {"result": True, "why": "{} {}".format(method, out)}
        else:
            logging.critical("Can't connect to a conference server")
            return {"reesult": False, "why": "Method not found..."}


class GreetingRecord(Resource):  # GET
    def get(self, room_vcb, dnis):
        conf = {}
        print dnis
        conf["ip"] = "65.48.98.217"
        if conf:
            con = ESL.ESLconnection(conf["ip"], '8021', 'ClueCon')
            exe = con.api("originate {{origination_caller_id_name={0},origination_caller_id_number=8000,ignore_early_media=true,room_vcb={0}}}sofia/internal/{1}@65.48.99.135 8000".format(room_vcb, dnis))
            out = exe.getBody()
            print out
            return {"result": True, "body": room_vcb}
        return {"result": False, "why": "Something went wrong"}


class GreetingPlayback(Resource):  # GET
    def get(self, room):
        condb = db.ncbDB()
        sql = "SELECT conf_room.vcb_id, vcb.greeting_path FROM vcb LEFT JOIN conf_room ON vcb.vcb_id = conf_room.vcb_id WHERE conf_room.room_id = {}".format(room)
        row = condb.ncb_getQuery(sql)
        if row:
            if len(row) == 1:
                rec = row[0]
                file_name = rec["greeting_path"]
                file_path = os.path.join(media_path, "greetings", rec["vcb_id"], file_name)
                if os.path.isfile(file_path):
                    content = send_from_directory(file_path, file_name, mimetype='audio/wav')
                    return {"resut": True, "filedata": {"filename": file_name, "data": content}}
        return {"result": False, "why": "Can't get data from DB or no such file"}

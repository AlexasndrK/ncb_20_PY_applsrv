"""
 Project code: FCONF
 Development code: NCB-20
 File: RECORDING.PY
 File location: ../flask-dev/resources/
 type: Python 2.7
 Description: Program module containing API functions referred to as Conference and Greetings Recording
 data in Web server features
"""
import ESL
import db
from datetime import datetime
from flask_restful import Resource
from models.eslConf import *

media_path = "/media/conference"


class Recording(Resource):  # GET
    def get(self, uuid):
        pass

    def delete(self, uuid):  # DELETE
        pass


class GetRecordings(Resource):  # GET
    def get(self, room):
        cdb = db.ncbDB()
        sql = "SELECT t1.room_id AS confroom, t1.id as uuid, t1.record_time, t1.file_path AS filelocation FROM conf_record t1 JOIN conf_room t2 ON t1.room_id = t2.rid  WHERE t2.room_id = {}".format(room)
        row = cdb.ncb_getQuery(sql)
        if len(row) >= 1:
            return row
        else:
            return {"result": False, "why": "Can't get list of records", "sql": sql}


class DoRecording(Resource):  # GET
    def get(self, method, room):
        conf = getConferenceIP(room)
        cdb = db.ncbDB()
        sql = "SELECT vcb, rid FROM con_room WHERE room_id = {}".format(room)
        row = cdb.ncb_getQuery(sql)
        vcb = row[0]
        uuid = getConfUUID(room)

        timestamp = datetime.now()
        rec_path = "{}/{}/records".format(media_path, vcb['vcb'])
        recfile = "{}/{}_rec_{}.wav".format(rec_path, room, timestamp)

        con = ESL.ESLconnection(ip, '8021', 'ClueCon')
        if con.connected:
            if method.strtoupper == 'START':
                pattern = "recording_node"
                if re.search(pattern, conf['body']) == false:
                    exe = con.api("conference conf_{} recording start {}".format(room, recfile))
                    sql = "INSERT INTO conf_record (room_id, file_path, uuid, record_time) VALUES ({}, {}, {}, {})".format(vcb['rid'], recfile, uuid, timestamp)
                    cdb.ncb_pushQuery(sql)
                    return {"result": True, "why": "Started {}".format(exe.getBody())}
                return {"result": False, "why": "Recording already started..."}
            elif method.strtoupper == 'STOP':
                sql = "SELECT id, file_path FROM conf_record WHERE uuid = {}".format(uuid)
                row = cdb.ncb_getQuery(sql)
                rec = row[0]
                sql = "update conf_record set uuid=NULL where id = {}".format(rec['id'])
                cdb.ncb_pushQuery(sql)
                exe = con.api("conference conf_{$confroom} recording stop {}".format(rec['file_path']))
                out = exe.getBody()
                return {"result": True, "why": "Stopped {}".format(out)}
            elif method.strtoupper == 'PAUSE':
                sql = "SELECT id, file_path, FROM conf_record  WHERE uuid = {}".format(uuid)
                row = cdb.ncb_getQuery(sql)
                rec = row[0]
                if rec:
                    exe = con.api("conference conf_{} recording pause {}".format(room, rec['file_path']))
                    out = exe.getBody()
                    return {"result": True, "why": "Paused {}".format(out)}
            else:
                sql = "SELECT id, file_path, FROM conf_record  WHERE uuid = {}".format(uuid)
                row = cdb.ncb_getQuery(sql)
                rec = row[0]
                if rec:
                    exe = con.api("conference conf_{} recording {} {}".format(room, method, rec['file_path']))
                    out = exe.getBody()
                    return {"result": True, "why": "{} {}".format(method, out)}
        else:
            logging.critical("Can't connect to a conference server")
            return {"reesult": False, "why": "Method not found..."}


class GreetingRecord(Resource):  # GET
    def get(self, dnis):
        pass

'''function greetingPlayback($confroom)
{
    if (file_exists("/mnt/nfs/sounds/$confroom.ulaw")) {
        $contents = file_get_contents("/mnt/nfs/sounds/$confroom.ulaw");
        $base64 = base64_encode($contents);
        return array("result" => true, "filedata" => array("filename" => "$confroom.ulaw",
                    "data" => $base64));
    } else {
        return array("result" => false);
    }
}'''
class GreetingPlayback(Resource):  # GET
    def get(self, room):
        pass

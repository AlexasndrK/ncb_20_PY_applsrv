

"""
 Project code: FCONF
 Development code: NCB-20
 File: FREESWITCH.PY
 File location: ../flask-dev/resources/
 type: Python 2.7
 Description: Program module containing API functions referred to as Conference room moderation features
"""
import db
from flask_restful import Resource
import ESL
import re
import xml.etree.ElementTree as ET

# EslServer = "65.48.98.217"


class UndeafConferenceRoom(Resource):
    def get(self, room):
        sql = "SELCT ip FROM servers"
        dbcon = db.ncbDB()
        eslServer = dbcon.ncb_getQuery(sql)
        for ip in [eslServer]:
            con = ESL.ESLconnection(str(ip['ip']), "8021", "ClueCon")
            if con.connected():
                exe = con.api("conference conf_{} undeaf non_moderator".format(room))
                out = exe.getBody()
        pattern = 'OK undeaf'
        if re.search(pattern, out):
            return {"result": True}
        return {"result": False}


class DeafConferenceRoom(Resource):
    def get(self, room):
        sql = "SELCT ip FROM servers"
        dbcon = db.ncbDB()
        eslServer = dbcon.ncb_getQuery(sql)
        for ip in [eslServer]:
            con = ESL.ESLconnection(str(ip['ip']), "8021", "ClueCon")
            if con.connected():
                exe = con.api("conference conf_{} deaf non_moderator".format(room))
                out = exe.getBody()
        pattern = 'OK deaf'
        if re.search(pattern, out):
            return {"result": True}
        return {"result": False}



class GetConferenceRoomInfo(Resource):
    def get(self, room):
        pass


class LockConferenceRoom(Resource):
    def get(self, room):
        sql = "SELCT ip FROM servers"
        dbcon = db.ncbDB()
        eslServer = dbcon.ncb_getQuery(sql)
        for ip in [eslServer]:
            con = ESL.ESLconnection(str(ip['ip']), "8021", "ClueCon")
            if con.connected():
                exe = con.api("conference conf_{} lock".format(room))
                out = exe.getBody()
        pattern = 'OK conf_{} locked'.format(room)
        if re.search(pattern, out):
            return {"result": True}
        return {"result": False}


class UnlockConferenceRoom(Resource):
    def get(self, room):
        sql = "SELCT ip FROM servers"
        dbcon = db.ncbDB()
        eslServer = dbcon.ncb_getQuery(sql)
        for ip in [eslServer]:
            con = ESL.ESLconnection(eslServer['ip'], "8021", "ClueCon")
            if con.connected():
                exe = con.api("conference conf_{} unlock".format(room))
                out = exe.getBody()
        pattern = "OK conf_{} unlocked".format(room)
        if re.search(pattern, out):
            return {"result": True}
        return {"result": False}


class Dial(Resource):
    def get(self, dnis, ani):
        pass


class MuteConferenceRoom(Resource):
    def get(self, room):
        sql = "SELCT ip FROM servers"
        dbcon = db.ncbDB()
        eslServer = dbcon.ncb_getQuery(sql)
        for ip in [eslServer]:
            con = ESL.ESLconnection(str(ip['ip']), "8021", "ClueCon")
            if con.connected():
                exe = con.api("conference conf_{} mute non_moderator".format(room))
                out = exe.getBody()
        pattern = 'OK mute'
        if re.search(pattern, out):
            return {"result": True}
        return {"result": False}


class UnmuteConferenceRoom(Resource):
    def get(self, room):
        sql = "SELCT ip FROM servers"
        dbcon = db.ncbDB()
        eslServer = dbcon.ncb_getQuery(sql)
        for ip in [eslServer]:
            con = ESL.ESLconnection(str(ip['ip']), "8021", "ClueCon")
            if con.connected():
                exe = con.api("conference conf_{} unmute non_moderator".format(room))
                out = exe.getBody()
        pattern = 'OK unmute'
        if re.search(pattern, out):
            return {"result": True}
        return {"result": False}


class ToggleMuteConferenceUser(Resource):
    def get(self, room, uuid):
        pass


class DeafConferenceUser(Resource):
    def get(self, room, uuid):
        pass


class UndeafConferenceUser(Resource):
    def get(self, room, uuid):
        pass


class GetBridges(Resource):
    def get(self, custid):
        $sql = "select a.dnis, a.confroom, b.confpass, b.confowner, b.confadminpin, b.maxuser, b.spinuser, b.spinmod from dnis2conf as a left join conference as b on a.confroom = b.confroom where b.confowner = '$custid'"
        pass

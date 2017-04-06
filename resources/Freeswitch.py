

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
from models.eslConf import *
import logging

# EslServer = "65.48.98.217"


class UndeafConferenceRoom(Resource):
    def get(self, room):
        conf = getConferenceIP(room)
        con = ESL.ESLconnection(conf['ip'], "8021", "ClueCon")
        if con.connected():
            exe = con.api("conference conf_{} undeaf non_moderator".format(room))
            out = exe.getBody()
        pattern = 'OK undeaf'
        if re.search(pattern, out):
            return {"result": True}
        return {"result": False}


class DeafConferenceRoom(Resource):
    def get(self, room):
        conf = getConferenceIP(room)
        con = ESL.ESLconnection(conf['ip'], "8021", "ClueCon")
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
        conf = getConferenceIP(room)
        con = ESL.ESLconnection(conf['ip'], "8021", "ClueCon")
        if con.connected():
            exe = con.api("conference conf_{} lock".format(room))
            out = exe.getBody()
        pattern = 'OK conf_{} locked'.format(room)
        if re.search(pattern, out):
            return {"result": True}
        return {"result": False}


class UnlockConferenceRoom(Resource):
    def get(self, room):
        conf = getConferenceIP(room)
        con = ESL.ESLconnection(conf['ip'], "8021", "ClueCon")
        if con.connected():
            exe = con.api("conference conf_{} unlock".format(room))
            out = exe.getBody()
        pattern = "OK conf_{} unlocked".format(room)
        if re.search(pattern, out):
            return {"result": True}
        return {"result": False}


class Dial(Resource):
    def get(self, room, dnis, ani):
        conf = getConferenceIP(room)
        if conf:
            con = ESL.ESLconnection(conf["ip"], '8021', 'CleCon')
            if con.connected:
                exe = con.api("originate sofia/external/$dnis@65.48.99.10 '&lua(confadd.lua {})'".format(room))
                out = exe.getBody()
                return {"result": True, "dialresult": out}
        logging.critical("Can't get any info")
        return {"result": False, "dialresult": "Couldnt connect to conference server"}


class MuteConferenceRoom(Resource):
    def get(self, room):
        conf = getConferenceIP(room)
        con = ESL.ESLconnection(conf['ip'], "8021", "ClueCon")
        if con.connected():
            exe = con.api("conference conf_{} mute non_moderator".format(room))
            out = exe.getBody()
        pattern = 'OK mute'
        if re.search(pattern, out):
            return {"result": True}
        return {"result": False}


class UnmuteConferenceRoom(Resource):
    def get(self, room):
        conf = getConferenceIP(room)
        con = ESL.ESLconnection(conf['ip'], "8021", "ClueCon")
        if con.connected():
            exe = con.api("conference conf_{} unmute non_moderator".format(room))
            out = exe.getBody()
        pattern = 'OK unmute'
        if re.search(pattern, out):
            return {"result": True}
        return {"result": False}


class ToggleMuteConferenceUser(Resource):
    def get(self, room, uuid):
        user = getUserIDbyUUID(room, uuid)
        con = ESL.ESLconnection(user['ip'], '8021', 'ClueCon')
        exe = con.api("conference conf_{} tmute {}".format(room, user['id']))
        out = exe.getBody()
        pattern = 'Ok'
        if re.search(pattern, out):
            return {"result": True, "what": out}
        return {"result": False, "what": out}


class DeafConferenceUser(Resource):
    def get(self, room, uuid):
        user = getUserIDbyUUID(room, uuid)
        if user:
            con = ESL.ESLconnection(user['ip'], '8021', "ClueCon")
            exe = con.api("conference conf_{} deaf {}".format(room, user['id']))
            out = exe.getBody()
            pattern = "Ok deaf"
            if re.search(pattern, out):
                return {"result": True}
        logging.critical("Can't connect to conferenct server")
        return {"result": False}


class UndeafConferenceUser(Resource):
    def get(self, room, uuid):
        user = getUserIDbyUUID(room, uuid)
        if user:
            con = ESL.ESLconnection(user['ip'], '8021', "ClueCon")
            exe = con.api("conference conf_{} undeaf {}".format(room, user['id']))
            out = exe.getBody()
            pattern = "Ok deaf"
            if re.search(pattern, out):
                return {"result": True}
        logging.critical("Can't connect to conferenct server")
        return {"result": False}


class GetBridges(Resource):
    def get(self, custid):
        # $sql = "select a.dnis, a.confroom, b.confpass, b.confowner, b.confadminpin, b.maxuser, #
        #    b.spinuser, b.spinmod from dnis2conf as a left join conference as b on a.confroom =
        # b.confroom #where b.confowner = '$custid'"
        pass



"""
 Project code: FCONF
 Development code: NCB-20
 File: FREESWITCH.PY
 File location: ../flask-dev/resources/
 type: Python 2.7
 Description: Program module containing API functions referred to as Conference room moderation features
"""

from flask_restful import Resource
from urllib import unquote
from models.eslConf import *
import ESL
import db
import re
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
        else:
            return {"result": False}


class GetConferenceRoomInfo(Resource):
    def get(self, room):
        conf = getConferenceIP(room)
        if conf:
            xmlp = etree.XML(conf['body'])
            xList = []
            xInDict = {}
            xDict = {"members": [{"member": ""}]}
            for node in xmlp.iter("member"):
                if node.attrib["type"] == "caller":
                    for elem in node:
                        if elem.tag == "caller_id_name":
                            name = getUserName(elem.text, room)
                            if name:
                                xInDict[elem.tag] = name
                            else:
                                xInDict[elem.tag] = unquote(elem.text)
                        elif elem.tag == "flags":
                            for flag in elem:
                                xInDict[flag.tag] = flag.text
                        else:
                            xInDict[elem.tag] = elem.text
                xList.append(xInDict)
            xDict["members"][0]["member"] = xList
            if xDict:
                return xDict
        return {"result": False}


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
        room = 'conf_' + room
        if conf:
            con = ESL.ESLconnection(conf["ip"], '8021', 'ClueCon')
            if con.connected:
                exe = con.api("originate {{origination_caller_id_name={},origination_caller_id_number={}}}sofia/internal/{}@65.48.99.135 '&lua(confadd.lua {})'".format(ani, ani, dnis, room))
                if exe:
                    out = exe.getBody()
                    pattern = "OK"
                    if re.search(pattern, out):
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


# Strange function does not understand from what
class GetBridges(Resource):
    def get(self, custid):
        sql = "SELECT a.dnis, a.confroom, b.confpass, b.confowner, b.confadminpin, b.maxuser, b.spinuser, b.spinmod FROM dnis2conf AS a LEFT JOIN conference AS b ON a.confroom = b.confroom WHERE b.confowner = {}".format(custid)
        cdb = db.ncbDB()
        row = cdb.ncb_getQuery(sql)
        if row:
            return row
        return {"result": False, "why": "Can't get any info from DB"}

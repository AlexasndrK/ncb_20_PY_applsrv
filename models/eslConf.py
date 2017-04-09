import ESL
from lxml import etree
import db
import logging
from urllib import unquote
logging.basicConfig(filename='test.log', level=logging.DEBUG)


def getConfUUID(room):
    conf = getConferenceIP(room)
    # con = ESL.ESLconnection(conf['ip'], '8021', 'ClueCon')
    # if con.connected():
    # exe = con.api("conference conf_{} xml_list".format(room))
    xml = etree.fromstring(conf['body'])
    element = xml.find("conference").get("uuid")
    if element:
        return element
    return False


def getUserIDbyUUID(room, uuid):
    conf = getConferenceIP(room)
    # con = ESL.ESLconnection(conf['ip'], '8021', 'ClueCon')
    # if con.connected():
    # exe = con.api("conference conf_{} xml_list".format(room))
    xml = etree.XML(conf['body'])
    _id = xml.xpath(".//member[uuid/text()='{}']/id/text()".format(uuid))
    if _id:
        return {'id': str(_id), 'ip': conf['ip']}
    return False


# From old function I have removed MaxCalls param
# because we check maxusers in other part
# TODO:
def getConferenceIP(room):
    dbcon = db.ncbDB()
    rip = ""
    sql = "SELECT ip FROM servers"
    result = dbcon.ncb_getQuery(sql)
    logging.critical(result)
    if result:
        for ip in result:
            logging.critical(ip['ip'])
            con = ESL.ESLconnection(str(ip['ip']), "8021", "ClueCon")
            if con.connected():
                exe = con.api("conference conf_{} xml_list".format(room))
                out = exe.getBody()
    # Maybe I need to move xml parsing to next part: for example if exe: break
                try:
                    xmlp = etree.fromstring(exe.getBody())
                except:
                    logging.critical("There is no such conference")
                    return False
                element = xmlp.find("conference").get("member-count")
                if element:
                    rip = str(ip['ip'])
        if rip == "":
            logging.critical("Error getting XML data from FS Server...")
            return False
        return {"ip": rip, "body": out}


def getUserName(caller, room):
    cdb = db.ncbDB()
    sql = "SELECT name FROM attendees_invited WHERE contact_phone_number = {} AND room_id = {}".format(caller, room)
    row = cdb.ncb_getQuery(sql)
    if row:
        if len(row) == 1:
            name = row[0]
            return name
    else:
        return False

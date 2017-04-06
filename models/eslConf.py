import ESL
from lxml import etree
import db
import logging

logging.basicConfig(filename='test.log',level=logging.DEBUG)

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
# TODO: Check What I will get if serves will have more than one row
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
        return {"ip": rip, "body": exe.getBody()}

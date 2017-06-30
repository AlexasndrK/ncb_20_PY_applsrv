from freeswitch import *
from time import sleep
import os
import db


def hangup_hook(session, what):
    consoleLog("info", "hangup hook for %s!!\n\n" % what)
    return


def handler(session, args):
    media_path = "/media/conference"
    session.answer()
    file_name = file_name = "{}_greeting.wav".format(args)
    room_vcb = args
    condb = db.ncbDB()
    if condb:
        if len(room_vcb) == 10:
            file_path = media_path + '/{}/greetings/{}'.format(room_vcb, file_name)
            sql = "UPDATE vcb SET greeting_path = '{}' WHERE vcb_id = '{}'".format(file_name, room_vcb)
        elif len(room_vcb) == 4:
            sql = "SELECT vcb_id FROM conf_room WHERE room_id = '{}'".format(room_vcb)
            row = condb.ncb_getQuery(sql)
            if row:
                vcb = row[0]["vcb_id"]
            else:
                return {"result": False, "why": "Check database for conf_room - {}".format(room_vcb)}
            file_path = media_path + '/{}/greetings/{}'.format(vcb, file_name)
            sql = "UPDATE conf_room SET greeting_path = '{}' WHERE room_id = '{}'".format(file_name, room_vcb)
            room_vcb = vcb

    if os.path.isfile(file_path):
        oldGreet = so.path.dirname(args) + '/old_greeting.wav'
        os.rename(file_path, oldGreet)
    consoleLog("info", "new greeting: %s" % args)
    while session.ready:
        consoleLog("info", "path: %s" % file_path)
        session.flushDigits()
        session.setVariable("playback_terminators", "#")
        dtmf = session.getDigits(1, "", 10000)

        if dtmf == '1':
            session.streamFile("/usr/local/freeswitch/share/freeswitch/sounds/en/us/callie/ivr/8000/ivr-begin_recording.wav")
            session.recordFile(file_path, 240, 500, 3)
            if os.path.isfile(file_path):
                consoleLog("info", "greeting recorded %s" % file_name)
            #    session.hangup()
        elif dtmf = '2':  # play file
            if os.path.isfile(args):
                session.streamFile(args)
            else:
                consoleLog("info", "No such file {}".format(args))
        elif dtmf = '3':  # confirm recording
            consoleLog("info", "record confirmed")
            cond.ncb_pushQuery(sql)
            return "Recorded successfully"
        else:
            # session.hangup()
            consoleLog("info", "You enter wrong comand")
    return False

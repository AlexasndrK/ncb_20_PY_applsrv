"""
 Project code: FCONF
 Development code: NCB-20
 File: APP.PY
 File location: ../flask-dev/
 type: Python 2.7
 Description: Flask dispatching engine at Application Server. It terminates REST API method and then routes it to
             correspondent module and function. It used to be handled a dialogue between WEB server and Appl server
"""


# TODO add import for new Resources. Before this we need to create new files which will contain all of them


from flask import Flask
from resources.IAC import *
from resources.Freeswitch import *
from resources.Provisioning import *
from resources.Recording import *

# from flask_jwt import JWT
from flask_restful import Api
app = Flask(__name__)
api = Api(app)
app.config['DEBUG'] = True

# con = ESL.ESLconnection('65.48.98.217', '8021', 'ClueCon')


# Simple for test purpose
@app.route('/')
def index():
    return "Hello World"


# Manupulations with user
api.add_resource(User, '/addUser', endpoint='adduser')  # POST - also can be used for GET and UPDATE
api.add_resource(User, '/checkUser/<string:user>', endpoint='checkuser')  # GET
api.add_resource(User, '/delUser/<string:user>', endpoint='deluser')  # DELETE
api.add_resource(ResetUserPassword, '/resetUserPassword')  # POST
api.add_resource(UserLogin, '/userLogin')  # POST
api.add_resource(GetUserConferences, '/getUserConferences/<string:user>')  # GET

# Manipulations with conference
api.add_resource(ProvisionConference, '/provisionConference', endpoint='provispost')  # POST
api.add_resource(ProvisionConference, '/provisionConference/<string:room>', endpoint='provisget')  # GET
api.add_resource(ProvisionConference, '/delConference/<string:confid>', endpoint='provisdel')  # DELETE maybe in one class
api.add_resource(UpdateProvisionConf, '/updateProvisionConference/')  # POST ?! - should be UPDATE or PUT
api.add_resource(GetAllConferenceRooms, '/GetAllConferenceRooms/<string:custid>')  # GET
api.add_resource(GetConferences, '/GetConferences/<string:vcb>')  # GET

# Manipulations with recordings: room recording and greeting recording
api.add_resource(Recording, '/getRecording/<string:uuid>', endpoint='recordget')  # GET
api.add_resource(Recording, '/delRecording/<string:uuid>', endpoint='recorddel')  # DELETE
api.add_resource(GetRecordings, '/getRecordings/<string:room>')  # GET
api.add_resource(DoRecording, '/doRecording/<string:method>/<string:room>')  # GET
api.add_resource(GreetingRecord, '/greetingRecord/<string:room>/<string:dnis>')  # GET
api.add_resource(GreetingPlayback, '/greetingPlayback/<string:room>')  # GET


# Manipulations with Freeswitch ESL API - room moderation
api.add_resource(UndeafConferenceRoom, '/undeafConferenceRoom/<string:room>')  # GET
api.add_resource(DeafConferenceRoom, '/deafConferenceRoom/<string:room>')  # GET
api.add_resource(GetConferenceRoomInfo, '/GetConferenceRoomInfo/<string:room>')  # GET
api.add_resource(LockConferenceRoom, '/lockConferenceRoom/<string:room>')  # GET
api.add_resource(UnlockConferenceRoom, '/unlockConferenceRoom/<string:room>')  # GET
api.add_resource(Dial, '/dial/<string:room>/<string:dnis>/<string:ani>')  # GET
api.add_resource(MuteConferenceRoom, '/muteConferenceRoom/<string:room>')  # GET
api.add_resource(UnmuteConferenceRoom, '/unmuteConferenceRoom/<string:room>')  # GET
api.add_resource(ToggleMuteConferenceUser, '/toggleMuteConferenceUser/<string:room>/<string:uuid>')  # GET
api.add_resource(DeafConferenceUser, '/deafConferenceUser/<string:room>/<string:uuid>')  # GET
api.add_resource(UndeafConferenceUser, '/undeafConferenceUser/<string:room>/<string:uuid>')  # GET
api.add_resource(GetBridges, '/getBridges/<string:custid>')  # GET


# We use it only for local run. For example for debuging purpose
if __name__ == '__main__':
    app.run(port=5000, debug=True)

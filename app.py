
"""
 Project code: FCONF
 Development code: NCB-20
 File: APP.PY
 File location: ../flask-dev/
 type: Python 2.7
 Description: Flask dispatching engine at Application Server. It terminates REST API method and then routes it to
             correspondent module and function. It used to be handled a dialogue between WEB server and Appl server
"""


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


# Simple for test purpose
@app.route('/')
def index():
    return "Hello World"


# Manupulations with user/userObject
api.add_resource(User, '/addUser', endpoint='adduser')  # POST - also can be used for GET and UPDATE
api.add_resource(User, '/checkUser/<string:user>', endpoint='checkuser')  # GET
api.add_resource(User, '/delUser/<string:user>', endpoint='deluser')  # DELETE
api.add_resource(ResetUserPassword, '/resetUserPassword')  # POST
api.add_resource(UserLogin, '/userLogin')  # POST
api.add_resource(GetUserConferences, '/getUserConferences/<string:user>')
api.add_resource(GetACobjectStart, '/getACobjectStart/<string:pid>/<string:role>')
api.add_resource(GetObjRCprofile, '/getObjRCprofile/<string:_type>/<string:objid>')
api.add_resource(GetObjAdminList, '/getObjAdminList/<string:_type>/<string:objid>')
api.add_resource(GetVCBlist, '/getVCBlist/<string:orgid>')

# Manipulations with conference
api.add_resource(ProvisionConference, '/provisionConference', endpoint='provispost')  # POST
api.add_resource(ProvisionConference, '/provisionConference/<string:room>', endpoint='provisget')  # GET
api.add_resource(ProvisionConference, '/delConference/<string:confid>', endpoint='provisdel')  # DELETE
api.add_resource(UpdateProvisionConf, '/updateProvisionConference/')  # POST ?! - should be UPDATE or PUT
api.add_resource(GetAllConferenceRooms, '/getAllConferenceRooms/<string:custid>')  # GET
api.add_resource(GetConfroombyVCB, '/getConfroombyVCB/<string:vcb>')  # GET
api.add_resource(GetObjectConfig, '/getConfig/<string:_type>/<string:_id>')
api.add_resource(ConfRoomAttributes, '/confRoomAttributes/<string:vcb_id>/<string:room_id>')
api.add_resource(Object, '/createObject', endpoint='objectcreate')
api.add_resource(Object, '/updatedObject', endpoint='objectupdate')
api.add_resource(Object, '/deleteObject/<string:pid>', endpoint='objectdelete')
api.add_resource(ObjectRP, '/createObjectRP', endpoint='objectprcreate')
api.add_resource(ObjectRP, '/updateObjectRP', endpoint='objectprupdate')
api.add_resource(ObjectRP, '/deleteObjectRP/<string:pid>', endpoint='objectprdelete')
api.add_resource(ModerAttributes, '/createModerAttributes', endpoint='modercreate')
api.add_resource(ModerAttributes, '/updateModerAttributes', endpoint='moderupdate')
api.add_resource(ModerAttributes, '/deleteModerAttributes/<string:pid>', endpoint='moderdelete')
api.add_resource(ConfRoom, '/createConfRoom', endpoint='createconfroom')
api.add_resource(ConfRoom, '/updateConfRoom', endpoint='updateconfroom')
api.add_resource(ConfRoom, '/deleteConfRoom/<string:rid>', endpoint='deleteconfroom')


# Manipulations with recordings: room recording and greeting recording
api.add_resource(Recording, '/getRecording/<string:uuid>', endpoint='recordget')  # GET
api.add_resource(Recording, '/delRecording/<string:uuid>', endpoint='recorddel')  # DELETE
api.add_resource(GetRecordings, '/getRecordings/<string:room>')  # GET
api.add_resource(DoRecording, '/doRecording/<string:method>/<string:room>')  # GET
api.add_resource(GreetingRecord, '/greetingRecord/<string:room_vcb>/<string:dnis>')  # GET
api.add_resource(GreetingPlayback, '/greetingPlayback/<string:room>')  # GET

#Manipulation with Users: Provisioning, Edit, Delete Users
api.add_resource(createUser, '/ProvisionUser') #POST
api.add_resource(editUser, '/ProvisionUser')  #PUT
api.add_resource(deleteUser, '/ProvisionUser')  #DELETE
api.add_resource(createUserAttributes, '/UserAttributes')  #POST
api.add_resource(editUserAtributes, '/UserAttributes') #PUT
api.add_resource(deleteUserAtributes, '/UserAttributes') #DELETE

#Manipulation with VCB: Create. edit, delete
api.add_resource(createVCB, '/ProvisionVCB')  #POST
api.add_resource(editVCB, '/ProvisionVCB')  #PUT
api.add_resource(deleteVCB, '/ProvisionVCB')  #DELETE

# Manipulations with Freeswitch ESL API - room moderation
api.add_resource(UndeafConferenceRoom, '/undeafConferenceRoom/<string:room>')
api.add_resource(DeafConferenceRoom, '/deafConferenceRoom/<string:room>')
api.add_resource(GetConferenceRoomInfo, '/getConferenceRoomInfo/<string:room>')
api.add_resource(LockConferenceRoom, '/lockConferenceRoom/<string:room>')
api.add_resource(UnlockConferenceRoom, '/unlockConferenceRoom/<string:room>')
api.add_resource(Dial, '/dial/<string:room>/<string:dnis>/<string:ani>')
api.add_resource(MuteConferenceRoom, '/muteConferenceRoom/<string:room>')
api.add_resource(UnmuteConferenceRoom, '/unmuteConferenceRoom/<string:room>')
api.add_resource(ToggleMuteConferenceUser, '/toggleMuteConferenceUser/<string:room>/<string:uuid>')
api.add_resource(DeafConferenceUser, '/deafConferenceUser/<string:room>/<string:uuid>')
api.add_resource(UndeafConferenceUser, '/undeafConferenceUser/<string:room>/<string:uuid>')
api.add_resource(GetBridges, '/getBridges/<string:custid>')



# We use it only for local run. For example for debuging purpose
if __name__ == '__main__':
    app.run(port=5000, debug=True)

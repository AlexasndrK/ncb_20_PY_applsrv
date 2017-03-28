"""
Project code: FCONF
Development code: NCB-20
File: NCBDISPATCHER.PY
File location: ../flask-dev/
type: Python 2.7
Description: Flask dispatching engine at Application Server. It terminates REST API method and then routes it to
            correspondent module and function. It used to be handled a dialogue between WEB server and Appl server
"""
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT   # not sure we really need it on the project
# project local modules
from moderation import *
from reflection import *
# from iac import *
# from provisioning import *

# PUT YOUR CODE BENEATH
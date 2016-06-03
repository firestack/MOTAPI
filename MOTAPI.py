##!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


# @app.errorhandler(Exception)
# def all_exception_handler(error):
#    return make_response(jsonify({'message': "Unknown Error"}), 500)

import Endpoints
API_VERSION = str(Endpoints.version)
API_ROOT = "/api/" + API_VERSION + "/"
USERS_ENDPOINT = API_ROOT + "users/<int:userID>/"

# Endpoints
from Endpoints.userinfo import UserInfo
from Endpoints.usermessages import UserMessages

api.add_resource(UserMessages, USERS_ENDPOINT + "messages")
api.add_resource(UserInfo, USERS_ENDPOINT, USERS_ENDPOINT + "info", endpoint="UserInfo")

if __name__ == '__main__':
	
	app.run(debug=True) 
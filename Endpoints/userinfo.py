from flask import jsonify, abort, make_response, request
from flask_restful import Resource

class UserInfo(Resource):
	def get(self, userID):
			args = request.args		

			return make_response(
				jsonify(
					{
					"user_id"	: userID,
					"username"	: str(userID),
					"banned"	: 110,
					"timedout"	: 10,
					"messages"	: 10
					}
				)
			)	
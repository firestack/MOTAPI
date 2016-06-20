from flask import jsonify, abort, make_response, request
from flask_restful import Resource


from . import MOTdb

class UserInfo(Resource):
	def get(self, userID):
			args = request.args
			messageCount = MOTdb.con.execute(
				"""SELECT COUNT(messages)
				FROM messages 
				WHERE userid = %s 
				""",
				userID
			)
			return make_response(
				jsonify(
					{
					
					"banned"	: 110,
					"timedout"	: 10,
					"messages"	: messageCount.fetchone()[0]
					}
				)
			)	
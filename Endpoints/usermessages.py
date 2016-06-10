from flask import jsonify, abort, make_response, request
from flask_restful import Resource

import json

from . import MOTdb

class UserMessages(Resource):
	NORMAL_REQUEST_LIMIT = 25
	MAX_REQUEST_LIMIT = 50

	def get(self, userID):
		args = request.args
		
		# Get and sanitize input
		offset = abs(int(args.get("offset", 0)))

		limit  = int(args.get("limit", UserMessages.NORMAL_REQUEST_LIMIT))
		limit  = (limit if limit < UserMessages.MAX_REQUEST_LIMIT else UserMessages.MAX_REQUEST_LIMIT)

		messages = MOTdb.con.execute("SELECT channel, message FROM messages WHERE userid = %s LIMIT %s OFFSET %s", userID, limit, offset)
		
		messages = [list(i) for i in messages.fetchall()]
		
		countOfMessages = MOTdb.con.execute("SELECT COUNT(message) FROM messages WHERE userid = %s", userID).fetchone()[0]


		return make_response(json.dumps({"args":args, "offset":offset, "limit":limit, "messages":messages, "count":countOfMessages}))
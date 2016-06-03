from flask import jsonify, abort, make_response, request
from flask_restful import Resource

class UserMessages(Resource):
	MAX_REQUEST_LIMIT = 25
	def get(self, userID):
		args = request.args
		
		# Get and sanitize input
		offset = int(args.get("offset", 0))
		offset = abs(offset)
		limit  = int(args.get("limit", 25))
		limit  = (limit if limit < UserMessages.MAX_REQUEST_LIMIT else UserMessages.MAX_REQUEST_LIMIT)

		return make_response(jsonify({"args":args, "offset":offset, "limit":limit}))
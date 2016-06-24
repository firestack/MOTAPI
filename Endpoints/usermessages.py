from flask import jsonify, abort, make_response, request, Response
from flask_restful import Resource

import json

from . import MOTdb

from datetime import datetime, date

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime) or isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    raise TypeError ("Type not serializable")

class UserMessages(Resource):
	NORMAL_REQUEST_LIMIT = 25
	MAX_REQUEST_LIMIT = 50

	def get(self, userID):
		args = request.args
		
		# Get and sanitize input
		offset = abs(int(args.get("offset", 0)))

		limit  = int(args.get("limit", UserMessages.NORMAL_REQUEST_LIMIT))
		limit  = (limit if limit < UserMessages.MAX_REQUEST_LIMIT else UserMessages.MAX_REQUEST_LIMIT)

		latest = args.get("latest", False)
		if (latest != False):
			latest = True

		latest = ("ASC" if latest else "DESC")

		# Make Query
		messages = MOTdb.con.execute(
			"""SELECT channel, message, created_at, id
			FROM messages 
			WHERE userid = %s 
			ORDER BY created_at {order} 
			LIMIT %s 
			OFFSET %s""".format(order=latest),
			userID, limit, offset
		)
		
		# Convert rows to dict
		messages = [
			dict(i)
			for i in messages.fetchall()
		]
		
		
		#countOfMessages = MOTdb.con.execute("SELECT COUNT(message) FROM messages WHERE userid = %s", userID).fetchone()[0]

		motjsonify = lambda data : Response(json.dumps(data, indent=None if request.is_xhr else 2, default=json_serial), mimetype='application/json')

		return motjsonify({"messages":messages})
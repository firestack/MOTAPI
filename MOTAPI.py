##!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Resource, Api
import sqlalchemy

app = Flask(__name__)
api = Api(app)


# @app.errorhandler(Exception)
# def all_exception_handler(error):
#    return make_response(jsonify({'message': "Unknown Error"}), 500)

import Endpoints
API_VERSION = str(Endpoints.version)
API_ROOT = "/api/" + API_VERSION + "/"
USERS_ENDPOINT = API_ROOT + "users/<int:userID>/"


from Endpoints import MOTdb


# Endpoints
from Endpoints.userinfo import UserInfo
from Endpoints.usermessages import UserMessages

api.add_resource(UserInfo, 		
	USERS_ENDPOINT, USERS_ENDPOINT + "info", 
	endpoint="UserInfo"
)

api.add_resource(UserMessages, 	
	USERS_ENDPOINT + "messages", 
	endpoint="UserMessages"
)

if __name__ == '__main__':
	import argparse
	import json


	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", 				default=False, 			help="Use Debug Mode", 			action="store_true"	)
	parser.add_argument("--threaded",			default=False, 			help="Experimental Threaded",   action="store_true"	)
	parser.add_argument("--host", 				default="0.0.0.0", 		help="Specify Host IP",			type=str			)
	parser.add_argument("--port", 				default=8443, 			help="Specify Host Port",		type=int			)
	parser.add_argument("--nossl", dest="ssl", 	default=True, 			help="Should Use SSL/HTTPS", 	action="store_false")
	parser.add_argument("--cfgfile",			default="config/cfg.json", 	help="Specify the configuration file", type=str 	)

	args = parser.parse_args()

	cfg = {}
	with open(args.cfgfile) as cfgin:
		cfg = json.load(cfgin)

	MOTdb.Start(cfg["sql"]["URL"])

	app_args = {"debug":args.debug, "host":args.host, "port":args.port, "threaded":args.threaded} 

	if args.ssl and cfg["SSL"].get("DISABLE", False):

		if cfg["SSL"]["SSLModule"] == "OpenSSL":
			from OpenSSL import SSL
			context = SSL.Context(SSL.SSLv23_METHOD)
			context.use_privatekey_file(cfg["SSL"]["private_key"])
			context.use_certificate_file(cfg["SSL"]["cert_file"])

		elif cfg["SSL"]["SSLModule"] == "SSL":
			import ssl
			context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
			context.load_cert_chain(cfg["SSL"]["cert_file"], cfg["SSL"]["private_key"])

		else:
			exit("SSL Not Loaded Properly")

		app.run(**app_args, ssl_context=context)

	else:
		app.run(**app_args) 
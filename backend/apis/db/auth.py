from flask import Response, request, jsonify
from flask_restplus import Resource, reqparse

from apis.db import api
from mongo import mongo

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import sys
import datetime

from jwt_auth.token import globalSecret, token_required, token_check_role


ns = api.namespace('auth', description="auth api")


######################
# GET TOKEN
######################
login_parser = reqparse.RequestParser()
login_parser.add_argument('usr', type=str, required=True)
login_parser.add_argument('pwd', type=str, required=True)

@ns.route("/")
@api.expect(login_parser)
class UserLogin(Resource):
    def post(self):
        args = login_parser.parse_args()
        usr = args["usr"]
        pwd = args["pwd"]

        coll = mongo.db.user
        res = coll.find_one({'name': usr})
        if res and check_password_hash(res['pwd'], pwd):

            token = jwt.encode({
                'user' : usr,
                'user_id' : res['id'],
                'role' : res['role'],
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60*12)}, 
                globalSecret
            )

            return {'msg': 'success', 'token': token.decode('UTF-8'), 'role' : res['role']}
        else:
            return {'msg': 'fail'}


test_parser = reqparse.RequestParser()
test_parser.add_argument('text', type=str, required=True)

######################
# HASH TEXT
######################
@ns.route('/test')
@api.expect(test_parser)
class AuthTest(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, data):
        args = test_parser.parse_args()
        text = args["text"]
        return {"ok": generate_password_hash(text) }, 200


@ns.route('/test/role')
class AuthTest2(Resource):
    @token_required
    @token_check_role
    @api.doc(security='apikey')
    def get(self, data):
        return {"msg": 'ok' }, 200


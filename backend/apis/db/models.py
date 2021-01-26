from flask import Response, request
from flask_restplus import Resource, reqparse

from apis.db import api
from mongo import mongo

from datetime import datetime

from jwt_auth.token import token_required, token_optional, token_check_role

ns = api.namespace('models', description="users api")

######################
# GET MODEL STATS
######################
@ns.route("/<string:name>")
class ModelStats(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _, name):
        coll = mongo.db.moderation
        result = coll.find_one({'name' : name}, {'_id' : 0})
        return {'data': result }

######################
# GET MODERATION STRATEGY
######################

@ns.route("/strategy/<string:name>")
class GetStrategy(Resource):
    @token_required
    @token_check_role
    @api.doc(security='apikey')
    def get(self, _, name):
        coll = mongo.db.moderation
        result = coll.find_one({'name' : name}, {'current_point' : 1})
        del result['_id']
        return {'data': result }

######################
# CHANGE MODERATION STRATEGY
######################

strategy_parser = reqparse.RequestParser()
strategy_parser.add_argument('name', type=str, required=True)
strategy_parser.add_argument('load', type=float, required=True)
strategy_parser.add_argument('acc', type=float, required=True)
strategy_parser.add_argument('eff', type=float, required=True)
strategy_parser.add_argument('unc', type=float, required=True)
strategy_parser.add_argument('s_name', type=str, required=True)

@ns.route("/strategy")
@api.expect(strategy_parser)
class UpdateStrategy(Resource):
    @token_required
    @token_check_role
    @api.doc(security='apikey')
    def post(self, _):
        coll = mongo.db.moderation
        args = strategy_parser.parse_args()
        name = args["name"]
        load = args["load"]
        acc = args["acc"]
        eff = args["eff"]
        unc = args["unc"]
        s_name = args["s_name"]
        if coll.find_one({'name' : name}):
            coll.update_one({'name' : name}, { "$set": {'current_point.load' : load, 'current_point.acc' : acc, 'current_point.eff' : eff, 'current_point.unc' : unc, 'current_point.name' : s_name}})
        return {'data' : 'ok'}, 200


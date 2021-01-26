from flask import Response, request
from flask_restplus import Resource, reqparse

from apis.db import api
from mongo import mongo

from datetime import datetime

from jwt_auth.token import token_required, token_optional

ns = api.namespace('users', description="users api")

######################
# GET USER STATS
######################
@ns.route("/stats/<string:name>")
class UserStats(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _, name):
        coll = mongo.db.comments
        result = list(coll.aggregate([
            { "$match": { "user_name" : name }},
            { "$group": { "_id": {"user_name" : "$user_name"}, 
                "count_recomendations": { "$sum": "$recommendations" }, 
                "count_comments": { "$sum": 1 },
                "count_comments_blocked": { "$sum": { "$cond": ["$blocked", 1, 0] } },
            }}
        ]))
        if result and len(result) > 0:
            obj = list(result)[0]
            del obj['_id']
            return {'data' : obj}
        return {'data' : {
            "count_recomendations": 0,
            "count_comments": 0
        }}

######################
# GET COMMENTS BY USER
######################

def getComments(name, mode):
    query = {'user_name': name, 'blocked': mode}
    coll = mongo.db.comments
    result_list = list(coll.find(query))
        
    for i in result_list:
        del i['_id'] 
        i['timestamp'] = i['timestamp'].isoformat() 
    return result_list

@ns.route("/comments/blocked/<string:name>")
class UserComments1(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _, name):
        return {'data': getComments(name, True)} 

@ns.route("/comments/valid/<string:name>")
class UserComments2(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _, name):
        return {'data': getComments(name, False)} 

@ns.route("/comments/undecided/<string:name>")
class UserComments3(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _, name):
        return {'data': getComments(name, None)}


######################
# GET USER NAMES
######################
@ns.route("/names/<string:search>")
class UserNames(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _, search):
        coll = mongo.db.comments
        result = coll.distinct( "user_name", { "user_name": { "$regex": search, '$options' : 'i' } } )
        result.sort()
        return {'data': result }


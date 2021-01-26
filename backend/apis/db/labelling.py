from flask import Response, request
from flask_restplus import Resource, reqparse

from apis.db import api
from mongo import mongo

from datetime import datetime

from jwt_auth.token import token_required, token_optional

ns = api.namespace('labelling', description="labelling api")

label_parser = reqparse.RequestParser()
label_parser.add_argument('id', type=int, required=True)
label_parser.add_argument('blocked', type=int, required=True)

######################
# label comment
######################
@ns.route("/label")
@api.expect(label_parser)
class LabelComment(Resource):
    @token_required
    @api.doc(security='apikey')
    def post(self, _):
        coll = mongo.db.comments

        args = label_parser.parse_args()
        cid = args["id"]
        blocked = args['blocked']

        coll.update_one({'id' : cid}, { "$set": {'ml.blocked': blocked, 'ml.uncertainty' : -1, 'ml.human' : 1 }})

        return {'data' : blocked}


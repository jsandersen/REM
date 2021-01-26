from flask import Response, request
from flask_restplus import Resource, reqparse


from apis.db import api
from mongo import mongo

from datetime import datetime

from jwt_auth.token import token_required, token_optional

ns = api.namespace('articles', description="articles api")

######################
# GET COMMENT BY ID
######################

article_parser = reqparse.RequestParser()
article_parser.add_argument('url', type=str, required=True)

@ns.route("/")
@api.expect(article_parser)
class GetCommentById(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        args = article_parser.parse_args()
        url = args['url']

        coll = mongo.db.articles
        result = coll.find_one({'url' : url}, {'_id' : 0, 'text' : 0})
        if result: 
            result['timestamp'] = result['timestamp'].isoformat() 
        return {'data': result}

######################
# COUNT ARTICLES
######################

@ns.route("/count")
class ArticleCounter(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        coll = mongo.db.articles
        return {'count': coll.find().count()}

######################
# COUNT ARTICLES BY TOPIC
######################


@ns.route("/topics/root/count")
class ArticleCounterRootTopic(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        coll =  mongo.db.articles
        query_obj = [
            #{ "$match": { "timestamp": { "$gte": datetime.strptime('2020-07-1', "%Y-%m-%d") } } },
            { "$group": { "_id": "$topic_root", "count": { "$sum": 1 } } },
            { "$sort": { "count": -1} }
        ]
        result = list(coll.aggregate(query_obj))

        return {'data': result, 'len': len(result)}

@ns.route("/topics/sub/count/<string:root_topic>")
class ArticleCounterSubTopic(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, root_topic, _):
        coll =  mongo.db.articles
        query_obj = [
            #{ "$match": { "topic_root" : root_topic,"timestamp": { "$gte": datetime.strptime('2020-07-1', "%Y-%m-%d") } } },
            { "$match": { "topic_root" : root_topic  } },
            { "$group": { "_id": "$topic_sub", "count": { "$sum": 1 } } },
            { "$sort": { "count": -1} }
        ]
        result = list(coll.aggregate(query_obj))

        return {'data': result, 'len': len(result)}

article_count_parser = reqparse.RequestParser()
article_count_parser.add_argument('flag', type=int)

@ns.route("/topics/root")
@api.expect(article_count_parser)
class ArticleTopic(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        coll =  mongo.db.articles
        args = article_count_parser.parse_args()

        flag = args.get("flag", None)
        if flag == 0:
            att = 'topic_root'
        else:
            att = 'title'        
        
        result = coll.distinct(att)
        #result.sort()
        return {'data': result }

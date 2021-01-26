from flask import Response, request
from flask_restplus import Resource, reqparse

from apis.db import api
from mongo import mongo

import pytz
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import sys
import os

from jwt_auth.token import token_required, token_optional

ns = api.namespace('comments', description="comments api")

tz = pytz.timezone('Europe/Paris')

TEST_DATA = os.environ.get('TEST_DATA')
start_time = datetime.strptime('2020-07-1', "%Y-%m-%d")

if TEST_DATA == "True":
    end_time = datetime.strptime('2020-07-21', "%Y-%m-%d")
else:
     end_time = datetime.now(tz=tz)

def getEndtime():
    return end_time

######################
# COUNT COMMENTS
######################

comment_count_parser = reqparse.RequestParser()
comment_count_parser.add_argument('blocked', type=int, required=False)
comment_count_parser.add_argument('uncertain', type=int, required=False)
comment_count_parser.add_argument('topic_root', type=str, required=False)
comment_count_parser.add_argument('user_name', type=str, required=False)
comment_count_parser.add_argument('article', type=str, required=False)
comment_count_parser.add_argument('time_slice', type=str, required=False)
comment_count_parser.add_argument('time', type=str, required=False)
comment_count_parser.add_argument('unc', type=float, required=True)
comment_count_parser.add_argument('human_mode', type=float)

@ns.route("/count")
@api.expect(comment_count_parser)
class Counter(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        coll = mongo.db.comments

        args = comment_count_parser.parse_args()
        blocked = args.get('blocked', None)
        uncertain = args.get('uncertain', None)
        topic_root = args.get('topic_root', None)
        user_name = args.get('user_name', None)
        article_title = args.get('article', None)
        time_slice = args.get("time_slice", None)
        time = args.get("time", None)
        unc = args.get("unc", None)
        human_mode = args.get("human_mode", None)

        obj={}
        coll = mongo.db.comments

        obj['ml'] = {'$exists' : 1}
        if uncertain is None and blocked is None:
            pass
        else:
            if uncertain:
                obj['ml.uncertainty'] = {'$gte' : unc}
            else:
                obj['ml.uncertainty'] = {'$lt' : unc}
        
        if blocked != None:
            obj['ml.blocked'] = blocked

        if human_mode != None and human_mode == 0:
            obj['ml.human'] = { '$not' : {'$exists' : 1}}

        if article_title !=None:
            obj['article_title'] = article_title

        if topic_root != None:
            obj['topic_root'] = topic_root

        if user_name != None:
            obj['user_name'] = user_name

        if time_slice != None:        
            start_date, end_date = getStartAndEndTime(time_slice)
            obj['timestamp'] = { "$gte": start_date, "$lt":  end_date}
        elif time:
            start = asTimestamp(time)
            obj['timestamp'] = { "$gte": start, "$lt":  getEndtime()}

        result = coll.find(obj).count()

        return {'count': result}

######################
# GET COMMENT BY ID
######################

@ns.route("/<int:id>")
class GetCommentById(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _, id):
        coll = mongo.db.comments
        result = coll.find_one({'id' : id})
        del result['_id']
        result['timestamp'] = result['timestamp'].isoformat() 
        return {'data': result}

######################
# GET Parents BY ID
######################

@ns.route("/parents/<int:id>")
class GetCommentRecById(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _, id):
        coll = mongo.db.comments
        comments = []
        root_comment = coll.find_one({'id' : id})
        if root_comment:
            del root_comment['_id']
            comments.insert(0, root_comment) 
            root_comment['timestamp'] = root_comment['timestamp'].isoformat()
            parent_id = root_comment['parent_id']
            while True:
                parent = coll.find_one({'id' : parent_id})
                if parent:
                    del parent['_id']
                    parent['timestamp'] = parent['timestamp'].isoformat()
                    comments.insert(0, parent) 
                    parent_id = parent.get('parent_id')
                else: 
                    break

        for i in range(len(comments)):
            comments[i]['i'] = i
        return {'data': comments}

######################
# COUNT DISTINCT USER 
######################

count_distinct_parser = reqparse.RequestParser()
count_distinct_parser.add_argument('time_slice', type=str)
count_distinct_parser.add_argument('time', type=str)

@ns.route("/user/count/distinct")
@api.expect(count_distinct_parser)
class CounterDistinctUser(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        coll =  mongo.db.comments

        args = count_distinct_parser.parse_args()
        time_slice = args.get("time_slice", None)
        time = args.get('time', None)

        query = {
             'ml' : {'$exists' : 1},
        }

        if time_slice:
            start_date, end_date = getStartAndEndTime(time_slice)
            query['timestamp'] = { "$gte": start_date, "$lt":  end_date}
        elif time:
            start = asTimestamp(time)
            query['timestamp'] = { "$gte": start, "$lt":  getEndtime()}

        res = len(coll.distinct('user_name', query)) # topic_root

        return {'data': res} 

######################
# COUNT DISTINCT TOPICS 
######################


@ns.route("/topics/count/distinct")
@api.expect(count_distinct_parser)
class CounterDistinctTopics(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        coll =  mongo.db.comments

        args = count_distinct_parser.parse_args()
        time_slice = args.get("time_slice", None)
        time = args.get('time', None)

        query = {
             'ml' : {'$exists' : 1},
        }

        if time_slice:
            start_date, end_date = getStartAndEndTime(time_slice)
            query['timestamp'] = { "$gte": start_date, "$lt":  end_date}
        elif time:
            start = asTimestamp(time)
            query['timestamp'] = { "$gte": start, "$lt":  getEndtime()}

        res = len(coll.distinct('topic_root', query))

        return {'data': res} 


######################
# COUNT DISTINCT ARTICLE
######################

@ns.route("/article/count/distinct")
@api.expect(count_distinct_parser)
class CounterDistinctArticle(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        coll =  mongo.db.comments

        args = count_distinct_parser.parse_args()
        time_slice = args.get("time_slice", None)
        time = args.get('time', None)

        query = {
             'ml' : {'$exists' : 1},
        }

        if time_slice:
            start_date, end_date = getStartAndEndTime(time_slice)
            query['timestamp'] = { "$gte": start_date, "$lt":  end_date}
        elif time:
            start = asTimestamp(time)
            query['timestamp'] = { "$gte": start, "$lt":  getEndtime()}

        res = len(coll.distinct('article_title', query))

        return {'data': res} 

######################
# COUNT COMMENTS BY USER
######################

from flask_restplus import reqparse

user_count_parser = reqparse.RequestParser()
user_count_parser.add_argument('sort', type=str)
user_count_parser.add_argument('topic_root', type=str)
user_count_parser.add_argument('selected_user', type=str)
user_count_parser.add_argument('page', type=int)
user_count_parser.add_argument('time_slice', type=str)
user_count_parser.add_argument('time', type=str)
user_count_parser.add_argument('unc', type=float)
user_count_parser.add_argument('flag', type=int, required=True)


@ns.route("/user/count/")
@api.expect(user_count_parser)
class CounterUser(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        coll =  mongo.db.comments

        args = user_count_parser.parse_args()
        sort = args.get("sort", None)
        topic_root = args.get("topic_root", None)
        selected_user = args.get("selected_user", None)
        page = args.get("page", 1)
        time_slice = args.get("time_slice", None)
        time = args.get('time', None)
        unc = args.get('unc', None)
        flag = args.get("flag", None)

        if flag == 0:
            att = 'topic_root'
        else:
            att = 'article_title'

        if not page or page <= 0:
            page = 1

        switcher = {
            "summe" : "total_comments",
            "offline" : "count_comments_blocked",
            "unsicher" : "count_comments_unknown",
            "online" : "count_comments_online"
        }

        query_obj = [
            { "$match": { #0
                'ml' : {'$exists' : 1}, 
                "timestamp": { "$gte": start_time, "$lt" : getEndtime() } } },
            { "$project": { #1
                '_id' : '$id', 
                'timestamp': '$timestamp', 
                'unc': {'$cond': [{'$gt': ['$ml.uncertainty', unc]}, 1, 0]}, 
                'user_name': '$user_name', 
                'ml' : '$ml' } },
            { "$group": { #2
                "_id": "$user_name", 
                "count_comments_blocked": {'$sum' : {'$cond': [{'$and': ['$ml.blocked', {'$not' : '$unc'}]}, 1, 0]} }, 
                "count_comments_unknown": {'$sum' : '$unc'}, 
                "total_comments": { "$sum": 1 }}},
            { "$project": { #3
                '_id' : '$_id', 
                'timestamp': '$timestamp', 
                'unc': '$unc', 
                'user_name': '$user_name', 
                'ml' : '$ml',
                "count_comments_blocked": '$count_comments_blocked', 
                "count_comments_unknown": '$count_comments_unknown', 
                "total_comments": '$total_comments',
                'count_comments_online' : { '$subtract': [ '$total_comments', { '$add': [ '$count_comments_blocked', '$count_comments_unknown' ] }  ] }
                } },
            { "$sort": { switcher.get(sort, "total_comments") : -1} }, #4
            { "$skip" : ((page - 1)  * 5) },
            { "$limit" : 5 }
        ]

        if topic_root:
            query_obj[0]["$match"][att] = topic_root

        if time_slice:
            start_date, end_date = getStartAndEndTime(time_slice)
            query_obj[0]['$match']['timestamp'] = { "$gte": start_date, "$lt":  end_date}
        elif time:
            start = asTimestamp(time)
            query_obj[0]['$match']['timestamp'] = { "$gte": start, "$lt":  getEndtime()}
            

        if selected_user:
            query_obj[0]["$match"]["user_name"] = { "$not": { "$eq": selected_user } }
            query_obj[5]["$skip"] = (page-1) * 4
            query_obj[6]["$limit"] = 4

            result1 = list(coll.aggregate(query_obj))

            query_obj[0]["$match"]["user_name"] = selected_user
            query_obj[5]["$skip"] = 0
            query_obj[6]["$limit"] = 1
            result2 = list(coll.aggregate(query_obj))

            if not result2:
                return { "data": { "series": [0, 0, 0], "categories": [selected_user] } }

            result1.insert(0, result2[0])

            result = result1

        else:
            result = list(coll.aggregate(query_obj))

        result = prepareVis(result)

        return {'data': result}

######################
# COUNT COMMENTS BY TOPIC
######################

topic_count_parser = reqparse.RequestParser()
topic_count_parser.add_argument('sort', type=str)
topic_count_parser.add_argument('user_name', type=str)
topic_count_parser.add_argument('selected_topic', type=str)
topic_count_parser.add_argument('page', type=int)
topic_count_parser.add_argument('time_slice', type=str)
topic_count_parser.add_argument('time', type=str)
topic_count_parser.add_argument('unc', type=float)
topic_count_parser.add_argument('flag', type=int, required=True)


@ns.route("/topics/root/count")
@api.expect(topic_count_parser)
class CounterRootTopic(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        coll =  mongo.db.comments

        args = topic_count_parser.parse_args()
        sort = args.get("sort", None)
        user_name = args.get("user_name", None)
        selected_topic = args.get("selected_topic", None)
        page = args.get("page", 1)
        time_slice = args.get("time_slice", None)
        time = args.get('time', None)
        unc = args.get('unc', None)
        flag = args.get('flag', 0)

        if not page or page <= 0:
            page = 1
        
        if flag == 0:
            att = 'topic_root'
        else:
            att = 'article_title'

        switcher = {
            "summe" : "total_comments",
            "offline" : "count_comments_blocked",
            "unsicher" : "count_comments_unknown",
            "online" : "count_comments_online"
        }

        query_obj = [
            { "$match": { 
                'ml' : {'$exists' : 1}, 
                "timestamp": { "$gte": start_time, "$lt" : getEndtime() } } },
            { "$project": { 
                '_id' : '$id', 
                'timestamp': '$timestamp', 
                'unc': {'$cond': [{'$gt': ['$ml.uncertainty', unc]}, 1, 0]}, 
                'topic_root': '$'+att, 
                'ml' : '$ml' } },
            { "$group": { 
                "_id": "$topic_root", 
                "count_comments_blocked": {'$sum' : {'$cond': [{'$and': ['$ml.blocked', {'$not' : '$unc'}]}, 1, 0]} }, 
                "count_comments_unknown": {'$sum' : '$unc'}, 
                "total_comments": { "$sum": 1 }}},
            { "$project": { 
                '_id' : '$_id', 
                'timestamp': '$timestamp', 
                'unc': '$unc', 
                'topic_root': '$topic_root', 
                'ml' : '$ml',
                "count_comments_blocked": '$count_comments_blocked', 
                "count_comments_unknown": '$count_comments_unknown', 
                "total_comments": '$total_comments',
                'count_comments_online' : { '$subtract': [ '$total_comments', { '$add': [ '$count_comments_blocked', '$count_comments_unknown' ] }  ] } } },
            { "$sort": { switcher.get(sort, "total_comments") : -1} },
            { "$skip" : ((page - 1)  * 5) },
            { "$limit" : 5 }
        ]

        if user_name:
            query_obj[0]["$match"]["user_name"] = user_name

        if time_slice:
            start_date, end_date = getStartAndEndTime(time_slice)
            query_obj[0]['$match']['timestamp'] = { "$gte": start_date, "$lt":  end_date}
        elif time:
            start = asTimestamp(time)
            query_obj[0]['$match']['timestamp'] = { "$gte": start, "$lt":  getEndtime()}

        if selected_topic:
            query_obj[0]["$match"][att] = { "$not": { "$eq": selected_topic } }
            query_obj[5]["$skip"] = (page-1) * 4
            query_obj[6]["$limit"] = 4
            result1 = list(coll.aggregate(query_obj))

            query_obj[0]["$match"][att] = selected_topic
            query_obj[5]["$skip"] = 0
            query_obj[6]["$limit"] = 1
            result2 = list(coll.aggregate(query_obj))

            if not result2:
                return { "data": { "series": [0, 0, 0], "categories": [selected_topic] } }

            result1.insert(0, result2[0])

            result = result1

        else:
            result = list(coll.aggregate(query_obj))
        
        result = prepareVis(result)
        return {'data': result, 'skip' : (page - 1)  * 5, 'limit' : 5}

article_count_parser = reqparse.RequestParser()
article_count_parser.add_argument('sort', type=str)
topic_count_parser.add_argument('user_name', type=str)
article_count_parser.add_argument('selected_article', type=str)
article_count_parser.add_argument('page', type=int)
article_count_parser.add_argument('time_slice', type=str)
article_count_parser.add_argument('time', type=str)
article_count_parser.add_argument('unc', type=float)

@ns.route("/article/count")
@api.expect(topic_count_parser)
class CounterArticle(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        coll =  mongo.db.comments

        args = topic_count_parser.parse_args()
        sort = args.get("sort", None)
        user_name = args.get("user_name", None)
        selected_article = args.get("selected_article", None)
        page = args.get("page", 1)
        time_slice = args.get("time_slice", None)
        time = args.get('time', None)
        unc = args.get('unc', None)

        if not page or page <= 0:
            page = 1

        switcher = {
            "summe" : "total_comments",
            "offline" : "count_comments_blocked",
            "unsicher" : "count_comments_unknown",
            "online" : "count_comments_online"
        }

        query_obj = [
            { "$match": { 
                'ml' : {'$exists' : 1}, 
                "timestamp": { "$gte": start_time, "$lt" : getEndtime() } } },
            { "$project": { 
                '_id' : '$id', 
                'timestamp': '$timestamp', 
                'unc': {'$cond': [{'$gt': ['$ml.uncertainty', unc]}, 1, 0]}, 
                'article_title': '$article_title', 
                'ml' : '$ml' } },
            { "$group": { 
                "_id": "$article_title", 
                "count_comments_blocked": {'$sum' : {'$cond': [{'$and': ['$ml.blocked', {'$not' : '$unc'}]}, 1, 0]} }, 
                "count_comments_unknown": {'$sum' : '$unc'}, 
                "total_comments": { "$sum": 1 }}},
            { "$project": { 
                '_id' : '$_id', 
                'timestamp': '$timestamp', 
                'unc': '$unc', 
                'article_title': '$article_title', 
                'ml' : '$ml',
                "count_comments_blocked": '$count_comments_blocked', 
                "count_comments_unknown": '$count_comments_unknown', 
                "total_comments": '$total_comments',
                'count_comments_online' : { '$subtract': [ '$total_comments', { '$add': [ '$count_comments_blocked', '$count_comments_unknown' ] }  ] }
                } },
            { "$sort": { switcher.get(sort, "total_comments") : -1} },
            { "$skip" : ((page - 1)  * 5) },
            { "$limit" : 5 }
        ]

        if user_name:
            query_obj[0]["$match"]["user_name"] = user_name

        if time_slice:
            start_date, end_date = getStartAndEndTime(time_slice)
            query_obj[0]['$match']['timestamp'] = { "$gte": start_date, "$lt":  end_date}
        elif time:
            start = asTimestamp(time)
            query_obj[0]['$match']['timestamp'] = { "$gte": start, "$lt":  getEndtime()}

        if selected_article:
            query_obj[0]["$match"]["article_title"] = { "$not": { "$eq": selected_article } }
            query_obj[4]["$skip"] = (page-1) * 4
            query_obj[5]["$limit"] = 4
            result1 = list(coll.aggregate(query_obj))

            query_obj[0]["$match"]["article_title"] = selected_article
            query_obj[4]["$skip"] = 0
            query_obj[5]["$limit"] = 1
            result2 = list(coll.aggregate(query_obj))

            result1.insert(0, result2[0])

            result = result1

        else:
            result = list(coll.aggregate(query_obj))
        
        result = prepareVis(result)
        return {'data': result, 'skip' : (page - 1)  * 5, 'limit' : 5}

@ns.route("/topics/sub/count/<string:root_topic>")
class CounterSubTopic(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _, root_topic):
        coll =  mongo.db.comments
        query_obj = [
            { "$match": { 
                "topic_root" : root_topic, 
                'ml' : {'$exists' : 1}, 
                "timestamp": { "$gte": start_time, "$lt" : getEndtime() } } },
            { "$group": { 
                "_id": "$topic_sub", 
                "count": { "$sum": 1 } } },
            { "$sort": { 
                "count": -1} }
        ]
        result = list(coll.aggregate(query_obj))
        
        return {'data': result}

######################
# GROUP COMMENTS BY TIME
######################

from flask_restplus import reqparse

topic_parser = reqparse.RequestParser()
topic_parser.add_argument('root_topic', type=str)
topic_parser.add_argument('sub_topic', type=str)
topic_parser.add_argument('user_name', type=str)
topic_parser.add_argument('time', type=str)
topic_parser.add_argument('unc', type=float)

topic_parser.add_argument('flag', type=int, required=True)


def fillTimeGapsMin(data, time_limit = None):
    data = data['series']
    #start_date = datetime(2020, 7, 1)
    #end_date = datetime.now()
    if time_limit:
        start_date = time_limit
    else :
        start_date = start_time
    end_date = getEndtime()

    result = []
    cat = []

    for e in data:
        while (start_date.strftime("%Y-%m-%d %H:%M")) < e['key']:
            d = start_date.strftime("%Y-%m-%d %H:%M")
            result.append({'Offline': 0, 'total': 0, 'Unsicher': 0, 'key': d, 'Online': 0})
            cat.append(d)
            start_date += relativedelta(minutes=1)
        start_date += relativedelta(minutes=1)
        result.append(e)
        cat.append(e['key'])
    while start_date < end_date:
        d = start_date.strftime("%Y-%m-%d %H:%M")
        result.append({'Offline': 0, 'total': 0, 'Unsicher': 0, 'key': d, 'Online': 0})
        cat.append(d)
        start_date += relativedelta(minutes=1)
        
    return { 'series' : result, 'categories' : cat }

def fillTimeGapsHour(data, time_limit = None):
    data = data['series']
    #start_date = datetime(2020, 7, 1)
    #end_date = datetime.now()
    if time_limit:
        start_date = time_limit
    else :
        start_date = start_time
    end_date = getEndtime()

    result = []
    cat = []

    for e in data:
        while (start_date.strftime("%Y-%m-%d %H")) < e['key']:
            d = start_date.strftime("%Y-%m-%d %H")
            result.append({'Offline': 0, 'total': 0, 'Unsicher': 0, 'key': d, 'Online': 0})
            cat.append(d)
            start_date += relativedelta(hours=1)
        start_date += relativedelta(hours=1)
        result.append(e)
        cat.append(e['key'])
    while start_date < end_date:
        d = start_date.strftime("%Y-%m-%d %H")
        result.append({'Offline': 0, 'total': 0, 'Unsicher': 0, 'key': d, 'Online': 0})
        cat.append(d)
        start_date += relativedelta(hours=1)
        
    return { 'series' : result, 'categories' : cat }

def fillTimeGapsDay(data, time_limit = None):
    data = data['series']
    #start_date = datetime(2020, 7, 1)
    #end_date = datetime.now()
    if time_limit:
        start_date = time_limit
    else:
        start_date = start_time
    end_date = getEndtime()

    result = []
    cat = []

    for e in data:
        while (start_date.strftime("%Y-%m-%d")) < e['key']:
            d = start_date.strftime("%Y-%m-%d")
            result.append({'Offline': 0, 'total': 0, 'Unsicher': 0, 'key': d, 'Online': 0})
            cat.append(d)
            start_date += relativedelta(days=1)
        start_date += relativedelta(days=1)
        result.append(e)
        cat.append(e['key'])
    while start_date < end_date:
        d = start_date.strftime("%Y-%m-%d")
        result.append({'Offline': 0, 'total': 0, 'Unsicher': 0, 'key': d, 'Online': 0})
        cat.append(d)
        start_date += relativedelta(days=1)
        
    return { 'series' : result, 'categories' : cat }
        
def fillTimeGapsMonth(data):
    data = data['series']

    #start_date = datetime(2020, 1, 1)
    #end_date = datetime.now()

    start_date =  start_time
    end_date = getEndtime()

    result = []
    cat = []

    for e in data:
        while start_date.strftime("%Y-%m") < e['key']:
            d = start_date.strftime("%Y-%m")
            result.append({'Offline': 99, 'total': 0, 'Unsicher': 0, 'key': d, 'Online': 0})
            cat.append(d)
            start_date += relativedelta(months=+1)
        start_date += relativedelta(months=+1)
        result.append(e)
        cat.append(e['key'])
    while start_date < end_date:
        d = start_date.strftime("%Y-%m")
        result.append({'Offline': 0, 'Unsicher': 0, 'Online': 0, 'total': 0, 'key': d, })
        cat.append(d)
        start_date += relativedelta(months=+1)
        
    return { 'series' : result, 'categories' : cat }

def groupByTime(t, root_topic, user_name, unc, att, time_limit = None):
    switcher = {
        'min': "%Y-%m-%d %H:%M",
        'h': "%Y-%m-%d %H",
        'd': "%Y-%m-%d",
        'm': "%Y-%m",
        'y': "%Y",
    }

    if time_limit:
        start = time_limit
    else:
        start = start_time

    time_filter =  switcher.get(t)
    query_obj = [
            { "$match": { 
                "timestamp": { "$gte": start, "$lt" : getEndtime() }, 
                "ml" : {'$exists' : 1} } },
            { "$project": { 
                '_id' : '$id', 
                'timestamp': '$timestamp', 
                'unc': {'$cond': [{'$gt': ['$ml.uncertainty', unc]}, 1, 0]}, 
                'topic_root': '$'+att, 
                'ml' : '$ml' } },
            { "$group": { 
                "_id": { "$dateToString": { "format": time_filter, "date": "$timestamp"} }, 
                "count_comments_blocked": {'$sum' : {'$cond': [{'$and': ['$ml.blocked', {'$not' : '$unc'}]}, 1, 0]} }, 
                "count_comments_unknown": {'$sum' : '$unc'}, "total_comments": { "$sum": 1 }}},
            { "$sort": { 
                "_id": 1 } }
        ]
    if root_topic:
        query_obj[0]["$match"][att] = root_topic

    if user_name:
        query_obj[0]["$match"]['user_name'] = user_name

    return query_obj

def prepareStackedBarchart(data):
    obj = []

    
    for i in data:
        obj.append({
            'Offline' : i['count_comments_blocked'],
            'Unsicher' : i['count_comments_unknown'],
            'Online' : i['total_comments'] - ( i['count_comments_unknown'] + i['count_comments_blocked']),
            'total' : i['total_comments'],
            'key' : str(i['_id'])
        })

    return { 
        "series": obj,
        #'categories' : map(lambda d: str(d['_id']), data)
        }

def prepareVis(data):
    val = []
    ids = []
    
    for i in data:
        val.append(i['count_comments_online'])
        val.append(i['count_comments_unknown'])
        val.append(i['count_comments_blocked'])
        if i['_id'] is None:
            ids.append('Sonstige')
        else:    
            ids.append(i['_id'])

    return { 
        "series": val,
        'categories' : ids
        }

def asTimestamp(time):
        now = getEndtime()
        if time == "1Std":
            return now - relativedelta(hours=1)
        elif time == "4Std": 
            return now - relativedelta(hours=4)
        elif time == "24Std": 
            return now - relativedelta(hours=24)
        elif time == "72Std": 
            return now - relativedelta(hours=72)
        #elif time == "1Woche": 
        #    return now - timedelta(weeks=1)
        else:
             return now - relativedelta(hours=72)

@ns.route("/group/min")
@api.expect(topic_parser)
class GroupByMin(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        args = topic_parser.parse_args()
        root_topic = args["root_topic"]
        user_name = args["user_name"]
        time = args["time"]
        unc = args["unc"]
        flag = args.get("flag", None)
        if flag == 0:
            att = 'topic_root'
        else:
            att = 'article_title'

        time_limit = asTimestamp(time)

        coll = mongo.db.comments
        result = list(coll.aggregate(groupByTime('min', root_topic, user_name, unc, att, time_limit)))
        result = prepareStackedBarchart(result)
        result = fillTimeGapsMin(result, time_limit)

        return {'data': result}

@ns.route("/group/hour")
@api.expect(topic_parser)
class GroupByHour(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        args = topic_parser.parse_args()
        root_topic = args["root_topic"]
        user_name = args["user_name"]
        time = args["time"]
        unc = args['unc']
        flag = args.get("flag", None)

        if flag == 0:
            att = 'topic_root'
        else:
            att = 'article_title'

        time_limit = asTimestamp(time)
        
        coll = mongo.db.comments
        result = list(coll.aggregate(groupByTime('h', root_topic, user_name, unc, att, time_limit)))
        result = prepareStackedBarchart(result)
        result = fillTimeGapsHour(result, time_limit)

        return {'data': result}

@ns.route("/group/day")
@api.expect(topic_parser)
class GroupByDay(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        args = topic_parser.parse_args()
        root_topic = args["root_topic"]
        user_name = args["user_name"]
        unc = args['unc']
        time = args["time"]

        flag = args.get("flag", None)
        if flag == 0:
            att = 'topic_root'
        else:
            att = 'article_title'

        time_limit = asTimestamp(time)

        coll = mongo.db.comments
        result = list(coll.aggregate(groupByTime('d', root_topic, user_name, unc, att, time_limit)))
        result = prepareStackedBarchart(result)
        result = fillTimeGapsDay(result, time_limit)

        return {'data': result}

@ns.route("/group/month")
@api.expect(topic_parser)
class GroupByMonth(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        args = topic_parser.parse_args()
        root_topic = args["root_topic"]
        user_name = args["user_name"]
        unc = args['unc']

        flag = args.get("flag", None)
        if flag == 0:
            att = 'topic_root'
        else:
            att = 'article_title'

        coll = mongo.db.comments
        result = list(coll.aggregate(groupByTime('m', root_topic, user_name, unc, att)))
        result = prepareStackedBarchart(result)

        return {'data': result}

@ns.route("/group/year")
@api.expect(topic_parser)
class GroupByYear(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        args = topic_parser.parse_args()
        root_topic = args["root_topic"]
        user_name = args["user_name"]
        unc = args['unc']

        flag = args.get("flag", None)
        if flag == 0:
            att = 'topic_root'
        else:
            att = 'article_title'

        coll = mongo.db.comments
        result = list(coll.aggregate(groupByTime('y', root_topic, user_name, att, unc)))
        result = prepareStackedBarchart(result)
        return {'data': result}

######################
# GET COMMENT OBJ
######################

comment_parser = reqparse.RequestParser()
comment_parser.add_argument('skip', type=int, required=True)
comment_parser.add_argument('limit', type=int, required=True)
comment_parser.add_argument('blocked', type=int, required=False)
comment_parser.add_argument('uncertain', type=float, required=False)
comment_parser.add_argument('topic_root', type=str, required=False)
comment_parser.add_argument('user_name', type=str, required=False)
comment_parser.add_argument('time_slice', type=str, required=False)
comment_parser.add_argument('time', type=str)
comment_parser.add_argument('unc', type=float)

comment_parser.add_argument('sort_key', type=int, required=False)
comment_parser.add_argument('sort_mode', type=int, required=False)

comment_parser.add_argument('flag', type=int, required=True)
comment_parser.add_argument('human_mode', type=int, required=False)


def getStartAndEndTime(time_slice):
    split = list(map(lambda x: int(x), time_slice.replace(' ','-').replace(':','-').split('-')))
    if len(split) == 5: # hour
        start_date = datetime(split[0], split[1], split[2], split[3], split[4])
        end_date = start_date + relativedelta(minutes=+1)   
    elif len(split) == 4: # hour
        start_date = datetime(split[0], split[1], split[2], split[3])
        end_date = start_date + relativedelta(hours=+1)    
    elif len(split) == 3: # day
        start_date = datetime(split[0], split[1], split[2])
        end_date = start_date + relativedelta(days=+1)
    elif len(split) == 2: #month
        start_date = datetime(split[0], split[1], 1)
        end_date = start_date + relativedelta(months=+1)
    elif len(split) == 1: # year
        start_date = datetime(split[0], 1, 1)
        end_date = start_date + relativedelta(years=+1)
    return start_date, end_date

sort_values = ['timestamp', 'ml.uncertainty', 'recommendations']

import sys

@ns.route("/")
@api.expect(comment_parser)
class getData(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        args = comment_parser.parse_args()
        skip = args['skip']
        limit = args['limit']
        blocked = args.get('blocked', None)
        uncertain = args.get('uncertain', None)
        topic_root = args.get('topic_root', None)
        user_name = args.get('user_name', None)
        time_slice = args.get("time_slice", None)
        time = args.get("time", None)
        unc = args.get("unc", None)
        flag = args.get("flag", None)
        human_mode = args.get("human_mode", None)

        sort_key = args.get("sort_key", None)
        sort_mode = args.get("sort_mode", None)

        
        if flag == 0:
            att = 'topic_root'
        else:
            att = 'article_title'

        sort = None
        if sort_key != None:
            sort=[(sort_values[sort_key], sort_mode)]

        obj={}
        coll = mongo.db.comments

        obj['ml'] = {'$exists' : 1}

        if uncertain is None and blocked is None:
            pass
        else:
            if uncertain:
                obj['ml.uncertainty'] = {'$gte' : unc}
            else:
                obj['ml.uncertainty'] = {'$lt' : unc}

        if blocked != None:
            obj['ml.blocked'] = blocked

        if topic_root != None:
            obj[att] = topic_root

        if user_name != None:
            obj['user_name'] = user_name

        if human_mode != None and human_mode == 0:
            obj['ml.human'] = { '$not' : {'$exists' : 1}}

        if time_slice != None:        
            start_date, end_date = getStartAndEndTime(time_slice)
            obj['timestamp'] = { "$gte": start_date, "$lt":  end_date}
        elif time:
            start = asTimestamp(time)
            obj['timestamp'] = { "$gte": start, "$lt":  getEndtime()}

        if sort:
            result = coll.find(obj).sort(sort).skip(skip).limit(limit)
        else:
            result = coll.find(obj).skip(skip).limit(limit)

        result_list = list(result)
        for i in result_list:
            del i['_id'] 
            i['timestamp'] = i['timestamp'].isoformat() 
        return {'data': result_list}

######################
# GET CHANGE
######################

change_parser = reqparse.RequestParser()
change_parser.add_argument('unc_old', type=float, required=True)
change_parser.add_argument('unc_new', type=float, required=True)

changeQuery = lambda unc: [
    { "$match": {
        "timestamp": { "$gte": getEndtime() - relativedelta(hours=72), "$lt" : getEndtime() },
        'ml' : {'$exists' : 1} } },
    { "$project": {
        '_id' : 1, 
        'unc': {'$cond': [{'$gt': ['$ml.uncertainty', unc]}, 1, 0]},
        'ml' : '$ml' } },
    { "$project": {
        '_id' : 1, 
        'unc' : '$unc',
        'blocked': {'$cond': [{'$and': ['$ml.blocked', {'$not' : '$unc'}]}, 1, 0]},
        'not_blocked': {'$cond': [{'$and': [{'$not' : '$ml.blocked'}, {'$not' : '$unc'}]}, 1, 0]},
        'ml' : '$ml' } },
    { "$group":  { 
        '_id' : None, 
        'sum_blocked' : { '$sum': "$blocked" }, 
        'sum_unc' : { '$sum': "$unc" }, 
        'sum_not_blocked' : { '$sum': '$not_blocked' } } } 
]

@ns.route("/change")
@api.expect(change_parser)
class GetChange(Resource):
    @token_required
    @api.doc(security='apikey')
    def get(self, _):
        coll = mongo.db.comments
        args = change_parser.parse_args()
        unc_old = args["unc_old"]
        unc_new = args["unc_new"]
        
        res_old = list(coll.aggregate(changeQuery(unc_old)))[0]
        res_new = list(coll.aggregate(changeQuery(unc_new)))[0]

        return {'data': { 'old' : res_old, 'new': res_new} }, 200 
from pymongo import MongoClient
import json
from random import randrange, random
import datetime 

client = MongoClient()

db = client.rem
articles_coll = db.articles
comments_coll = db.comments
user_coll = db.user
moderation_coll = db.moderation

###
user_coll.drop()
moderation_coll.drop()
articles_coll.drop()
comments_coll.drop()

####
#### Create User 
####

with open('user.json') as json_file:
    user_obj = json.load(json_file)


user_coll.insert_one(user_obj)
print('User inserted')

####
#### Create Modelstats
####

with open('moderation.json') as json_file:
    moderation_obj = json.load(json_file)

moderation_coll.insert_one(moderation_obj)
print('Moderation inserted')


###
### Articles & Comments
###

startDate = datetime.datetime(2020, 7, 17, 0, 0)

articles = {
    0: (None, 'http://...', None, 'anonymous', 'German Autobahn', 'How German Autobahns changed the world', 'Few other landmarks represent Germany more than its freeway system', startDate),
    1: (None, 'http://...', None, 'anonymous', 'Travelling in Germany', 'What you need to know about travel in Germany', "Here's what we know about travelling in Germany, abroad and what politicians are saying.", startDate),
    2: (None, 'http://...', None, 'anonymous', 'DFB', 'Revealed: The next big change coming to DFB', 'Major change which will shape the line-ups at every club from next summer.', startDate),
}

topics = {
    0 : 'Travel',
    1 : 'Sport'
}

articles2topic = {
    0:0,
    1:0,
    2:1,
}

users = {
    0:'Karl',
    1:'Lisa',
    2:'Otto',
    3:'Anne',
    4:'Pia',
    5:'Marie',
    6:'Angela',
    7:'Mario'
}

n_comments = 5000

def random_date(start,l):
   current = start
   while l >= 0:
      curr = current + datetime.timedelta(days=randrange(4), hours=randrange(24), minutes=randrange(60))
      yield curr
      l-=1

###
### Create Articles
###
for key, value in articles.items():
    article_obj = {
        'url': value[1],
        'text': value[2],
        'timestamp': value[7],
        'author': value[3],
        'kicker' : value[4],
        'title': value[5],
        'summary': value[6],
        'topic_root' : topics[articles2topic[key]],
        'topic_sub': 'None'
    }
    articles_coll.insert_one(article_obj)

print('Articles inserted')

###
### Create Comments
###

def create_rnd_text():
    chars = "             abcdefghijklmnopqrstuvwxyz"
    text = []
    for i in range(50+ randrange(500)):
        text.append(chars[randrange(len(chars))])
    return "sample comment: " + "".join(text)

i = -1
for date in random_date(startDate,n_comments):
    i += 1

    article_id = randrange(len(articles))
    topic_id = articles2topic[randrange(len(articles))]
    user_id = randrange(len(users))

    rnd = random()
    ml_obj = { # simplified
        'p_blocked' : rnd,
        'uncertainty' : (1 - max(rnd, 1-rnd))*2, 
        'blocked': 1 if rnd >= 0.5 else 0,
    }

    comment_obj = {
        'id' : i,
        'user_name' : users[user_id],
        'text_history' : [create_rnd_text()],
        'parent_id': None,
        'recommendations' : randrange(10),
        'article' : articles[article_id][1],
        'article_title' : articles[article_id][5],
        'topic_root' : topics[articles2topic[article_id]],
        'topic_sub': 'None',
        'ml' : ml_obj,
        'timestamp': date
    }

    comments_coll.insert_one(comment_obj)
print('Comments inserted')

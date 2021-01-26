from flask import Blueprint
from flask_restplus import Api

from jwt_auth import authorization

blueprint = Blueprint('db_api', __name__)

api = Api(authorizations=authorization, version='1.0', title='User-Comments-API', description="An API for usercomments")
api.init_app(blueprint)

from apis.db.comments import ns as comments_namespace
from apis.db.articles import ns as articles_namespace
from apis.db.users import ns as users_namespace
from apis.db.models import ns as models_namespace
from apis.db.labelling import ns as labelling_namespace
from apis.db.auth import ns as auth_namespace

api.add_namespace(comments_namespace)
api.add_namespace(articles_namespace)
api.add_namespace(users_namespace)
api.add_namespace(models_namespace)
api.add_namespace(labelling_namespace)
api.add_namespace(auth_namespace)

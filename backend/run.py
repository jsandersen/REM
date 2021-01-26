#!/usr/bin/env python

import os
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask
from flask_cors import CORS
from mongo import mongo

from apis.db import blueprint as db_blueprint

# Mongo settings
MONGO_URI = os.environ.get('MONGO_URI')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
    
app = Flask(__name__)
app.config['MONGO_DBNAME'] = MONGO_DBNAME
app.config['MONGO_URI'] = MONGO_URI + MONGO_DBNAME
app.config['RESTPLUS_VALIDATE'] = True
app.config['RESTPLUS_MASK_SWAGGER'] = False


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app.wsgi_app = ReverseProxied(app.wsgi_app)
CORS(app)
mongo.init_app(app)

app.register_blueprint(db_blueprint, url_prefix='/db')

@app.route("/")
def hello():
    return "Flask"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
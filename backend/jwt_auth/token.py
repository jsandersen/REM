from functools import wraps
from flask import request
import jwt
import sys
import os

globalSecret = os.environ.get('JWT_SECRET')

def returnErrorMsg(msg):
    return {'message' : msg}, 401

def checkIfTokenExists(token):
    return token is not None

def checkIfTokenIsValidAndGetData(token):
    try:
        return True, jwt.decode(token, globalSecret)
    except: 
        return False, None


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers['x-access-token'] if 'x-access-token' in request.headers else None
        data = None
        
        if not checkIfTokenExists(token):
            return returnErrorMsg('Token is missing.')

        success, data = checkIfTokenIsValidAndGetData(token)
        if not success:
            return returnErrorMsg('Token is invalid.')

        return func(data, *args, **kwargs)

    return decorated

def check_role(token):
    success, data = checkIfTokenIsValidAndGetData(token)
    if success:
        role = data.get('role', '')
        if role == 'admin':
            return True
    return False


def token_check_role(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers['x-access-token'] if 'x-access-token' in request.headers else None
        data = None

        success = check_role(token)
        if not success:
            return returnErrorMsg('Access Denied.')

        return func(*args, **kwargs)

    return decorated

def token_optional(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers['x-access-token'] if 'x-access-token' in request.headers else None
        data = None

        success, data = checkIfTokenIsValidAndGetData(token)

        return func(data, *args, **kwargs)

    return decorated

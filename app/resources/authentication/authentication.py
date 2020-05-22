from functools import wraps
from flask import request, Response
import os


def check_auth(token):
    return token == os.getenv('APPLICATION_KEY', default='42')


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        else:
            token = None
        if not token or not check_auth(token):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

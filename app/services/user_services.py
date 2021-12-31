

from os import uname
from sqlalchemy.sql.base import NO_ARG
from app.models.user import User


def create_new_user(request_json):
    '''
    Register new user in WS DataBase and generate a token
    '''
    # Check if the request_json contain all user information
    if 'user_name' not in request_json:
        return None
    elif 'password' not in request_json:
        return None

    # Check if the username exits
    user = User.query.filter(User.user_name == request_json['user_name']).first()
    if user:
        return None
    # Create a new user in DB    
    user = User(request_json['user_name'], request_json['password'])
    user.save()
    return user


def autenticate_user(request_json):
    '''
    Autenticate a user with the credentials of request_json
    ''' 
    # Check if the request contain all user information
    if 'user_name' not in request_json:
        return None
    elif 'password' not in request_json:
        return None
    
    # Find the user
    user = User.query.filter(User.user_name == request_json['user_name']).first()
    # Check if exits the user
    if not user:
        return None
    # Validate the password
    if not user.check_hash(request_json['password']):
        return None
    return user
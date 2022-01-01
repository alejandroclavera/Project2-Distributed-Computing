import jwt
import os
import datetime
from functools import wraps
from flask import request, g, jsonify
from app.models.user import User

class Auth:
    """
    Auth Class
    """
    @staticmethod
    def generate_token(user_id):
        """
        Generate Token Method
        """ 
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }  
            # Generate the token
            return jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                'HS256'
            )
        except Exception as e:
            return None

    @staticmethod
    def decode_token(token):
        """
        Decode token method
        """
        response = {}
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), 'HS256')
            response['data'] = {'user_id': payload['sub']}
            return response
        except jwt.ExpiredSignatureError:
            response['error'] = {'message': 'token expired'}
            return response
        except jwt.InvalidTokenError:
            response['error'] = {'message': 'Invalid token'}
            return response
    
    @staticmethod
    def auth_required(func):
        """
        Authentication decorator        
        """
        @wraps(func)
        def decorated_auth(*args, **kargs):
            # Check the header contiain the user-token header
            if 'user-token' not in request.headers:
                return jsonify({'error': 'Authentication token is not available, please login to get one'}), 401
            
            # Get the user-token
            token = request.headers['user-token']
            data = Auth.decode_token(token)
            if 'error' in data:
                return jsonify({'error': data['error']}), 400

            # Get the user
            user_id = data['data']['user_id']
            user = User.get_user_by_id(user_id)
            if not user:
                return jsonify({'error': 'Invalid token, user does not exist'}), 400
            
            g.user = {'id': user_id}
            return func(*args, **kargs)
        return decorated_auth
            
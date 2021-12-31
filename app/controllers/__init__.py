from functools import wraps
from flask import request, jsonify

def require_request_json_body(func):
    @wraps(func)
    def require_json_body_func(*args, **kargs):
        if not request.json:
            return jsonify({'error': 'Bad request, the request must contain json body'}), 400
        return func(*args, **kargs)
    return require_json_body_func
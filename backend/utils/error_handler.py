# backend/utils/error_handler.py
from flask import jsonify
from functools import wraps

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            error_type = type(e).__name__
            
            response = {
                'error': True,
                'type': error_type,
                'message': error_message
            }
            
            status_code = 500
            if error_type == 'NotFound':
                status_code = 404
            elif error_type == 'ValidationError':
                status_code = 400
            
            return jsonify(response), status_code
    return wrapper
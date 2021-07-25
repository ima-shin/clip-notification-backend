import functools
from flask import request, make_response, jsonify


def content_type(value):
    """check content-type decorator"""
    def _content_type(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            c_type = request.headers.get('Content-Type')
            if not c_type == value:
                error_message = {
                    'error': 'not supported Content-Type'
                }
                return make_response(jsonify(error_message), 400)

            return func(*args, **kwargs)
        return wrapper
    return _content_type

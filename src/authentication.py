from functools import wraps
from flask import request, jsonify
import jwt
from initialize_db import env
from models import User


def token_auth(auth):
    """Token authentication

    Args:
        auth

    Returns:
        decorator
    """
    @wraps(auth)
    def decorator(*args, **kwargs):
        """Checks if token is valid

        Returns:
            auth: if token is valid
        """
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token,  env.str('SECRET_KEY'))
            user = User.query.filter_by(id=data['id']).first()
            current_user = user
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'Token is invalid'}), 401

        return auth(current_user, *args, **kwargs)

    return decorator

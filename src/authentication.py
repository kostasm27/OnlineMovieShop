from functools import wraps
from flask import request, jsonify
import jwt
from initialize_db import pgConn, env


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
            conn = pgConn.cursor()
            conn.execute(f"SELECT * from users where id = {data['id']}")
            row = conn.fetchall()
            current_user = row[0]
            conn.close()
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'Token is invalid'}), 401

        return auth(current_user, *args, **kwargs)

    return decorator

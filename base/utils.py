import datetime
import jwt
from django.conf import settings


def generate_access_token(user):
    expire_date = datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60)
    access_token_payload = {
        'username': user.username,
        'exp': expire_date,
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token, expire_date


def generate_refresh_token(user):
    refresh_token_payload = {
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token

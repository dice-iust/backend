import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_access_token(user):
    payload = {
        'user_id': user.user_id,
        'exp': datetime.utcnow() + timedelta(days=1),  # Token expiration in 1 day
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
